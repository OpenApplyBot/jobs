"""Google Careers scraper using the official public jobs search and detail pages.

Google's current careers URLs use /applications/jobs/results/ for listings,
numeric /results/N/ paths for result pages, and /results/<job-id>-<slug> for
individual roles. Pagination is discovered from the page's own next-page links.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urlunparse, parse_qsl, urlencode
import json
import os
import re
import threading
import time

import requests

from .common import normalize, location_text

COMPANY_NAME = "Google"
CAREERS_URL = "https://www.google.com/about/careers/applications/jobs/results/1/"
OFFICIAL_DOMAIN = "google.com"
CSV_RANK = 1

TIMEOUT = (5, max(8, int(os.getenv("GOOGLE_HTTP_TIMEOUT", "20"))))
MAX_PAGES = max(1, int(os.getenv("GOOGLE_MAX_PAGES", "250")))
DETAIL_WORKERS = max(1, min(8, int(os.getenv("GOOGLE_DETAIL_WORKERS", "5"))))
FETCH_DETAILS = os.getenv("GOOGLE_FETCH_DETAILS", "0").lower() not in {"0", "false", "no"}
USER_AGENT = (
    "OpenApplyBot-Jobs/1.0 (+https://github.com/OpenApplyBot/jobs; "
    "public job indexer)"
)
_local = threading.local()


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.text = []
        self.jsonld = []
        self._href = None
        self._anchor_text = []
        self._anchor_attrs = {}
        self._skip = 0
        self._script = False
        self._script_buf = []
        self._script_type = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style", "noscript"}:
            self._skip += 1
        if tag == "a" and attrs.get("href"):
            self._href = attrs["href"]
            self._anchor_text = []
            self._anchor_attrs = attrs
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._script = True
            self._script_buf = []

    def handle_data(self, data):
        value = " ".join(data.split())
        if value and not self._skip:
            self.text.append(value)
            if self._href is not None:
                self._anchor_text.append(value)
        if self._script:
            self._script_buf.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._anchor_text).strip(), self._anchor_attrs))
            self._href = None
            self._anchor_text = []
            self._anchor_attrs = {}
        if tag == "script":
            if self._script:
                self.jsonld.append("".join(self._script_buf))
                self._script = False
            if self._skip:
                self._skip -= 1
        elif tag in {"style", "noscript"} and self._skip:
            self._skip -= 1


def _session():
    if not hasattr(_local, "session"):
        session = requests.Session()
        session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json",
            "Accept-Language": "en-US,en;q=0.9",
        })
        _local.session = session
    return _local.session


def _google_url(url):
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    return parsed.scheme in {"http", "https"} and (
        host == "google.com" or host.endswith(".google.com")
    )


def _fetch(url):
    response = _session().get(url, timeout=TIMEOUT, allow_redirects=True)
    response.raise_for_status()
    if not _google_url(response.url):
        raise ValueError(f"Refusing unexpected off-domain redirect: {response.url}")
    parser = _Parser()
    parser.feed(response.text)
    return response.url, parser


def _clean(value):
    if value is None:
        return None
    if isinstance(value, dict):
        return value.get("name") or value.get("value") or value.get("text") or value.get("html")
    if isinstance(value, list):
        return ", ".join(filter(None, (_clean(item) for item in value)))
    return re.sub(r"\s+", " ", str(value)).strip() or None


def _walk_jobpostings(value):
    if isinstance(value, list):
        for item in value:
            yield from _walk_jobpostings(item)
    elif isinstance(value, dict):
        typ = value.get("@type", [])
        if typ == "JobPosting" or (isinstance(typ, list) and "JobPosting" in typ):
            yield value
        for key in ("@graph", "mainEntity", "itemListElement"):
            if key in value:
                yield from _walk_jobpostings(value[key])


def _jobpostings(parser):
    for raw in parser.jsonld:
        try:
            payload = json.loads(raw)
        except (ValueError, TypeError):
            continue
        yield from _walk_jobpostings(payload)


def _job_id(url):
    match = re.search(r"/results/(\d+)-", urlparse(url).path)
    return match.group(1) if match else None


def _is_job_url(url):
    path = urlparse(url).path
    return bool(re.search(r"/applications/jobs/results/\d+-.+", path, re.I))


def _is_listing_url(url):
    path = urlparse(url).path.rstrip("/")
    return bool(re.search(r"/applications/jobs/results(?:/\d+)?$", path, re.I))


def _canonical_job_url(url):
    parsed = urlparse(url)
    # Google job URLs are identified by their job ID and slug, not search filters.
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))


def _listing_urls(parser, page_url):
    jobs = {}
    for href, label, attrs in parser.links:
        absolute = urljoin(page_url, href)
        if not _google_url(absolute) or not _is_job_url(absolute):
            continue
        job_url = _canonical_job_url(absolute)
        job_id = _job_id(job_url)
        if not job_id:
            continue
        if label and label.lower() not in {"learn more", "apply", "apply now", "share"}:
            title = label
        else:
            title = None
        jobs.setdefault(job_url, {"url": job_url, "source_job_id": job_id, "title": title})
    return jobs


def _next_page(parser, current_url, visited):
    candidates = []
    for href, label, attrs in parser.links:
        absolute = urljoin(current_url, href)
        if not _google_url(absolute) or not _is_listing_url(absolute):
            continue
        if _is_job_url(absolute):
            continue
        path = urlparse(absolute).path.rstrip("/")
        # The site's numbered result pages use /results/1/, /results/2/, etc.
        match = re.search(r"/results/(\d+)$", path)
        if not match:
            continue
        number = int(match.group(1))
        rel = (attrs.get("rel") or "").lower()
        aria = (attrs.get("aria-label") or "").lower()
        label_lower = (label or "").lower()
        if "next" in rel or "next" in aria or "next page" in label_lower or "go to next page" in label_lower or "navigate_next" in label_lower:
            candidates.append((number, absolute))
    if candidates:
        for _, url in sorted(candidates):
            if url not in visited:
                return url

    # Some page versions expose numbered page links without an explicit next label.
    numbered = []
    for href, label, attrs in parser.links:
        absolute = urljoin(current_url, href)
        if not _google_url(absolute) or not _is_listing_url(absolute) or _is_job_url(absolute):
            continue
        match = re.search(r"/results/(\d+)$", urlparse(absolute).path.rstrip("/"))
        if match and absolute not in visited:
            numbered.append((int(match.group(1)), absolute))
    if numbered:
        current_match = re.search(r"/results/(\d+)$", urlparse(current_url).path.rstrip("/"))
        current_number = int(current_match.group(1)) if current_match else 0
        later = sorted((number, url) for number, url in numbered if number > current_number)
        if later:
            return later[0][1]
    return None


def _location_from_job(job):
    value = job.get("jobLocation") or job.get("applicantLocationRequirements")
    return location_text(value)


def _normalize_jsonld(job, page_url, listing=None):
    listing = listing or {}
    identifier = job.get("identifier")
    if isinstance(identifier, dict):
        identifier = identifier.get("value") or identifier.get("name")
    url = urljoin(page_url, _clean(job.get("url")) or page_url)
    if not _google_url(url):
        url = page_url
    title = _clean(job.get("title")) or listing.get("title")
    if not title:
        return None
    organization = job.get("hiringOrganization")
    if isinstance(organization, dict):
        company = organization.get("name") or COMPANY_NAME
    else:
        company = _clean(organization) or COMPANY_NAME
    description = job.get("description")
    if isinstance(description, dict):
        description = description.get("text") or description.get("html")
    job_id = identifier or _job_id(url) or listing.get("source_job_id")
    if not job_id:
        return None
    return normalize(
        str(job_id), title, url,
        location=_location_from_job(job) or listing.get("location"),
        department=job.get("occupationalCategory") or job.get("industry") or listing.get("department"),
        employment_type=job.get("employmentType"),
        description=description,
        posted_at=job.get("datePosted"),
        company=company,
        raw_payload=job,
        apply_url=url,
    )


def _detail(item):
    url = item["url"]
    try:
        final_url, parser = _fetch(url)
    except (requests.RequestException, ValueError) as exc:
        print(f"[Google] Detail page failed: {url}: {exc}", flush=True)
        return None
    for job in _jobpostings(parser):
        row = _normalize_jsonld(job, final_url, item)
        if row:
            return row

    text = " ".join(parser.text)
    # Google's detail route often includes the full job description as visible text.
    title = item.get("title")
    if not title:
        for href, label, attrs in parser.links:
            if label and label.lower() not in {"back to jobs search", "learn more", "share", "apply"}:
                if len(label) > 8 and not _is_listing_url(urljoin(final_url, href)):
                    title = label
                    break
    if not title:
        slug = urlparse(final_url).path.rsplit("/", 1)[-1]
        title = re.sub(r"^\d+-", "", slug).replace("-", " ").strip().title()
    location_match = re.search(
        r"(?:place|location)\s+([^|]{2,160}?(?:,\s*[A-Za-z]{2,}|\bRemote\b))",
        text, re.I
    )
    location = location_match.group(1).strip() if location_match else item.get("location")
    # Keep a bounded detail-text description; avoid saving the entire repeated result list.
    description = None
    markers = [
        r"Minimum qualifications",
        r"About the job",
        r"About the role",
        r"Responsibilities",
        r"Preferred qualifications",
    ]
    starts = [m.start() for pattern in markers if (m := re.search(pattern, text, re.I))]
    if starts:
        description = text[min(starts):]
        end = re.search(r"(?:Equal opportunity|Google is proud|Share this job|Back to jobs search)", description, re.I)
        if end:
            description = description[:end.start()]
        description = description[:40000].strip() or None
    raw = {
        "source": "Google Careers official job detail page",
        "job_id_from_url": _job_id(final_url),
        "detail_url": final_url,
        "structured_data_found": False,
        "visible_text_excerpt": text[:12000],
    }
    return normalize(
        _job_id(final_url) or item["source_job_id"], title, final_url,
        location=location,
        description=description,
        company=COMPANY_NAME,
        raw_payload=raw,
        apply_url=final_url,
    )


def scrape(token: str | None = None):
    """Fetch Google's public job listings, follow all discovered result pages, enrich details.

    Environment:
      GOOGLE_MAX_PAGES=250       maximum listing pages (20 jobs/page; default covers 5,000)
      GOOGLE_DETAIL_WORKERS=5    concurrent detail requests (1-8)
      GOOGLE_FETCH_DETAILS=1     optional detail-enrichment mode (slower)
    """
    start = (token or "").strip() or CAREERS_URL
    if not _google_url(start):
        raise ValueError(f"Refusing non-Google URL: {start}")
    if _is_job_url(start):
        item = {"url": _canonical_job_url(start), "source_job_id": _job_id(start), "title": None}
        row = _detail(item)
        return [row] if row else []

    if not _is_listing_url(start):
        start = CAREERS_URL

    print(f"[Google] Starting official careers scrape: {start}", flush=True)
    pending = [start]
    visited = set()
    listings = {}
    total_hint = None

    while pending and len(visited) < MAX_PAGES:
        page_url = pending.pop(0)
        if page_url in visited:
            continue
        visited.add(page_url)
        try:
            final_url, parser = _fetch(page_url)
        except (requests.RequestException, ValueError) as exc:
            print(f"[Google] Listing page failed: {page_url}: {exc}", flush=True)
            continue

        page_jobs = _listing_urls(parser, final_url)
        before = len(listings)
        for url, item in page_jobs.items():
            listings.setdefault(url, item)
        text = " ".join(parser.text)
        count_match = re.search(r"(\d[\d,]*)\s+jobs\s+matched", text, re.I)
        if count_match:
            total_hint = int(count_match.group(1).replace(",", ""))
        range_match = re.search(r"Showing\s+(\d+)\s+to\s+(\d+)\s+of\s+(\d+)", text, re.I)
        if range_match:
            total_hint = int(range_match.group(3))
        print(
            f"[Google] Page {len(visited)}: {len(page_jobs)} job links, "
            f"{len(listings)} unique listings" +
            (f" / {total_hint} reported" if total_hint is not None else ""),
            flush=True,
        )

        next_url = _next_page(parser, final_url, visited)
        if next_url and next_url not in pending and next_url not in visited:
            pending.append(next_url)
        # Do not fabricate page URLs if the site doesn't expose a next link.
        # This avoids looping over invalid numbered routes after a redesign.

    if not listings:
        print("[Google] No job detail links found on the official results page.", flush=True)
        return []

    items = list(listings.values())
    if not FETCH_DETAILS:
        output = []
        for item in items:
            row = normalize(
                item["source_job_id"], item.get("title") or "Untitled role",
                item["url"], company=COMPANY_NAME,
                raw_payload={"source": "Google Careers listing", "listing_only": True},
                apply_url=item["url"],
            )
            if row:
                output.append(row)
        print(f"[Google] Listing-only mode returned {len(output)} jobs", flush=True)
        return output

    print(f"[Google] Enriching {len(items)} job pages using {DETAIL_WORKERS} workers", flush=True)
    output = {}
    with ThreadPoolExecutor(max_workers=DETAIL_WORKERS) as executor:
        futures = {executor.submit(_detail, item): item for item in items}
        for index, future in enumerate(as_completed(futures), 1):
            try:
                row = future.result()
                if row:
                    output[row["source_job_id"]] = row
            except Exception as exc:
                print(f"[Google] Unexpected detail error: {futures[future]['url']}: {exc}", flush=True)
            if index % 50 == 0 or index == len(futures):
                print(f"[Google] Details processed: {index}/{len(futures)}; normalized jobs: {len(output)}", flush=True)

    print(
        f"[Google] Complete: {len(output)} normalized jobs from {len(listings)} listings "
        f"(reported total: {total_hint if total_hint is not None else 'unknown'})",
        flush=True,
    )
    return list(output.values())
