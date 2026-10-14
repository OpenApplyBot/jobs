"""Public job-board API connectors.

Connectors intentionally use documented/public endpoints. Keep requests bounded,
identify this client, and respect each provider's terms and rate limits.
"""
from html import unescape
import re
import requests

TIMEOUT = 25
HEADERS = {"User-Agent": "OpenApplyBot-Jobs/0.2 (+https://github.com/OpenApplyBot/jobs)"}


def clean(value):
    if not value:
        return None
    if isinstance(value, dict):
        value = value.get("html", value.get("text", ""))
    value = re.sub(r"<[^>]+>", " ", str(value))
    value = unescape(value)
    return re.sub(r"\s+", " ", value).strip() or None


def get_json(url, *, params=None, headers=None):
    response = requests.get(url, params=params, headers={**HEADERS, **(headers or {})}, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def normalize(job_id, title, url, location=None, department=None, employment_type=None,
              description=None, posted_at=None, company=None):
    if not job_id or not title or not url:
        return None
    return {
        "source_job_id": str(job_id), "title": str(title).strip() or "Untitled",
        "location": clean(location), "department": clean(department),
        "employment_type": clean(employment_type), "description": clean(description),
        "url": url, "posted_at": str(posted_at) if posted_at else None,
        "company_name": clean(company),
    }


def fetch_jobs(connector, token):
    token = token.strip()
    jobs = []

    # Employer ATS APIs
    if connector == "greenhouse":
        data = get_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs", params={"content": "true"})
        for j in data.get("jobs", []):
            item = normalize(j.get("id"), j.get("title"), j.get("absolute_url"),
                (j.get("location") or {}).get("name"),
                ", ".join(d.get("name", "") for d in j.get("departments", []) if d.get("name")),
                description=j.get("content"), posted_at=j.get("updated_at"))
            if item: jobs.append(item)
        return jobs

    if connector == "lever":
        data = get_json(f"https://api.lever.co/v0/postings/{token}", params={"mode": "json"})
        for j in data if isinstance(data, list) else []:
            c = j.get("categories") or {}
            item = normalize(j.get("id") or j.get("applyUrl"), j.get("text"), j.get("hostedUrl") or j.get("applyUrl"),
                c.get("location"), c.get("department"), c.get("commitment"),
                j.get("descriptionPlain") or j.get("description"), j.get("createdAt"))
            if item: jobs.append(item)
        return jobs

    if connector == "ashby":
        data = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}")
        for j in data.get("jobs", []):
            item = normalize(j.get("id") or j.get("jobUrl"), j.get("title"), j.get("jobUrl") or j.get("applyUrl"),
                j.get("location"), j.get("department") or j.get("team"), j.get("employmentType"),
                j.get("descriptionHtml") or j.get("description"), j.get("publishedAt"))
            if item: jobs.append(item)
        return jobs

    if connector == "smartrecruiters":
        offset = 0
        while offset < 5000:
            data = get_json(f"https://api.smartrecruiters.com/v1/companies/{token}/postings",
                            params={"limit": 100, "offset": offset})
            rows = data.get("content", [])
            for j in rows:
                loc = j.get("location") or {}
                item = normalize(j.get("id"), j.get("name"), j.get("ref"),
                    ", ".join(filter(None, [loc.get("city"), loc.get("region"), loc.get("country")])),
                    (j.get("department") or {}).get("label"), (j.get("typeOfEmployment") or {}).get("label"),
                    posted_at=j.get("releasedDate"))
                if item: jobs.append(item)
            if len(rows) < 100: break
            offset += len(rows)
        return jobs

    if connector == "workable":
        data = get_json(f"https://www.workable.com/api/accounts/{token}?details=true")
        rows = data.get("jobs", []) if isinstance(data, dict) else []
        for j in rows:
            loc = j.get("location") or {}
            item = normalize(j.get("shortcode") or j.get("id"), j.get("title"), j.get("url"),
                ", ".join(filter(None, [loc.get("city"), loc.get("region"), loc.get("country")])),
                j.get("department"), j.get("employment_type"), j.get("description"), j.get("created_at"))
            if item: jobs.append(item)
        return jobs

    if connector == "recruitee":
        data = get_json(f"https://{token}.recruitee.com/api/offers")
        rows = data.get("offers", []) if isinstance(data, dict) else []
        for j in rows:
            locs = j.get("locations") or []
            loc = ", ".join(filter(None, [x.get("city") or x.get("name") for x in locs if isinstance(x, dict)]))
            item = normalize(j.get("id"), j.get("title"), j.get("careers_url") or j.get("url"),
                loc, j.get("department"), j.get("employment_type"), j.get("description"), j.get("created_at"))
            if item: jobs.append(item)
        return jobs

    # Public multi-employer job APIs; token is a keyword or "all".
    if connector == "remoteok":
        data = get_json("https://remoteok.com/api")
        rows = data[1:] if isinstance(data, list) and data else []
        for j in rows:
            if not isinstance(j, dict): continue
            if token.lower() not in ("all", "*") and token.lower() not in (str(j.get("position", "")) + " " + str(j.get("company", "")) + " " + str(j.get("tags", ""))).lower(): continue
            item = normalize(j.get("id") or j.get("slug"), j.get("position"), j.get("url"),
                j.get("location") or "Remote", j.get("tags") and ", ".join(j["tags"]),
                j.get("job_type"), j.get("description"), j.get("date"), j.get("company"))
            if item: jobs.append(item)
        return jobs

    if connector == "remotive":
        params = {"search": "" if token.lower() in ("all", "*") else token, "limit": 100}
        data = get_json("https://remotive.com/api/remote-jobs", params=params)
        for j in data.get("jobs", []):
            item = normalize(j.get("id"), j.get("title"), j.get("url"), j.get("candidate_required_location") or "Remote",
                j.get("category"), j.get("job_type"), j.get("description"), j.get("publication_date"), j.get("company_name"))
            if item: jobs.append(item)
        return jobs

    if connector == "arbeitnow":
        page = 1
        while page <= 20:
            data = get_json("https://www.arbeitnow.com/api/job-board-api", params={"page": page})
            rows = data.get("data", [])
            for j in rows:
                searchable = f"{j.get('title','')} {j.get('company_name','')} {' '.join(j.get('tags') or [])}"
                if token.lower() not in ("all", "*") and token.lower() not in searchable.lower(): continue
                item = normalize(j.get("slug") or j.get("url"), j.get("title"), j.get("url"),
                    j.get("location") or ("Remote" if j.get("remote') else None),
                    ", ".join(j.get("tags") or []), description=j.get("description"),
                    posted_at=j.get("created_at"), company=j.get("company_name"))
                if item: jobs.append(item)
            if not data.get("links", {}).get("next") or not rows: break
            page += 1
        return jobs

    if connector == "themuse":
        page = 0
        while page < 20:
            data = get_json("https://www.themuse.com/api/public/jobs", params={"page": page, "descending": "true"})
            rows = data.get("results", [])
            for j in rows:
                locs = j.get("locations") or []
                loc = ", ".join(x.get("name", "") for x in locs if isinstance(x, dict))
                company = (j.get("company") or {}).get("name")
                searchable = f"{j.get('name','')} {company or ''}"
                if token.lower() not in ("all", "*") and token.lower() not in searchable.lower(): continue
                item = normalize(j.get("id"), j.get("name"), j.get("refs", {}).get("landing_page"),
                    loc, (j.get("categories") or [{}])[0].get("name") if j.get("categories") else None,
                    description=j.get("contents"), posted_at=j.get("publication_date"), company=company)
                if item: jobs.append(item)
            if not rows: break
            page += 1
        return jobs

    if connector == "jobicy":
        params = {"count": 50}
        if token.lower() not in ("all", "*"): params["tag"] = token
        data = get_json("https://jobicy.com/api/v2/remote-jobs", params=params)
        for j in data.get("jobs", []):
            item = normalize(j.get("id"), j.get("jobTitle"), j.get("url"), j.get("jobGeo") or "Remote",
                j.get("jobIndustry"), j.get("jobType"), j.get("jobDescription"), j.get("pubDate"), j.get("companyName"))
            if item: jobs.append(item)
        return jobs

    if connector == "himalayas":
        data = get_json("https://himalayas.app/jobs/api")
        rows = data if isinstance(data, list) else data.get("jobs", [])
        for j in rows:
            searchable = f"{j.get('title','')} {j.get('companyName','')} {j.get('excerpt','')}"
            if token.lower() not in ("all", "*") and token.lower() not in searchable.lower(): continue
            item = normalize(j.get("id") or j.get("slug"), j.get("title"), j.get("applicationLink") or j.get("url"),
                j.get("location") or "Remote", j.get("category"), j.get("employmentType"),
                j.get("description") or j.get("excerpt"), j.get("pubDate") or j.get("publishedAt"), j.get("companyName"))
            if item: jobs.append(item)
        return jobs


    if connector == "jsonld":
        # A single public careers page URL. Extract JobPosting JSON-LD without
        # executing JavaScript or attempting to bypass access controls.
        from html.parser import HTMLParser
        from urllib.parse import urljoin, urlparse
        import json

        class JsonLdParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.capture = False
                self.parts = []
                self.blocks = []
            def handle_starttag(self, tag, attrs):
                if tag.lower() == "script" and dict(attrs).get("type", "").lower() == "application/ld+json":
                    self.capture = True
                    self.parts = []
            def handle_data(self, data):
                if self.capture:
                    self.parts.append(data)
            def handle_endtag(self, tag):
                if tag.lower() == "script" and self.capture:
                    self.blocks.append("".join(self.parts))
                    self.capture = False

        start = token
        parsed = urlparse(start)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("jsonld board_token must be a public http(s) careers page URL")
        queue = [start]
        visited = set()
        while queue and len(visited) < 10:
            page = queue.pop(0)
            if page in visited:
                continue
            visited.add(page)
            response = requests.get(page, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            parser = JsonLdParser()
            parser.feed(response.text)
            for block in parser.blocks:
                try:
                    parsed_data = json.loads(block)
                except (ValueError, TypeError):
                    continue
                records = parsed_data if isinstance(parsed_data, list) else [parsed_data]
                for record in records:
                    if not isinstance(record, dict):
                        continue
                    if record.get("@type") == "JobPosting":
                        org = record.get("hiringOrganization") or {}
                        loc = record.get("jobLocation") or []
                        if isinstance(loc, dict): loc = [loc]
                        locations = []
                        for entry in loc:
                            address = entry.get("address") or {} if isinstance(entry, dict) else {}
                            if isinstance(address, dict):
                                locations.append(", ".join(filter(None, [address.get("addressLocality"), address.get("addressRegion"), address.get("addressCountry")])))
                        item = normalize(record.get("identifier", {}).get("value") if isinstance(record.get("identifier"), dict) else record.get("identifier") or record.get("url"),
                            record.get("title"), record.get("url") or page, ", ".join(filter(None, locations)),
                            record.get("industry") or record.get("occupationalCategory"),
                            record.get("employmentType"), record.get("description"),
                            record.get("datePosted"), org.get("name") if isinstance(org, dict) else None)
                        if item: jobs.append(item)
            # Follow same-site links only; limit total pages to avoid crawling a whole site.
            if len(visited) < 10:
                for href in re.findall(r'href=["\\']([^"\\']+)["\\']', response.text, flags=re.I):
                    absolute = urljoin(page, unescape(href))
                    target = urlparse(absolute)
                    if target.scheme in ("http", "https") and target.netloc == parsed.netloc and absolute not in visited and absolute not in queue:
                        if any(part in absolute.lower() for part in ("career", "jobs", "position", "opening")):
                            queue.append(absolute)
        # Deduplicate multiple structured-data copies of the same posting.
        unique = {}
        for item in jobs:
            unique[item["source_job_id"]] = item
        return list(unique.values())

    raise ValueError(f"Unsupported connector: {connector}")
