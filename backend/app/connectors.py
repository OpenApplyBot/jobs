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
    return re.sub(r"\\s+", " ", value).strip() or None


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

    raise ValueError(f"Unsupported connector: {connector}")
