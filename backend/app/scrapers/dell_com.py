"""Dell Technologies Careers scraper using the public Radancy/TalentBrew results endpoint."""
from __future__ import annotations
import html
import os
import re
import requests
from urllib.parse import urlsplit, urljoin
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Dell Technologies"
CAREERS_URL = "https://jobs.dell.com/en/search-jobs/india%20general/375/1/1"
API_URL = "https://jobs.dell.com/search-jobs/results"
OFFICIAL_DOMAIN = "jobs.dell.com"
CSV_RANK = 30
MAX_PAGES = max(1, min(10, int(os.getenv("DELL_MAX_PAGES", "2"))))
PAGE_SIZE = max(1, min(20, int(os.getenv("DELL_PAGE_SIZE", "20"))))
KEYWORDS = tuple(x.strip() for x in os.getenv("DELL_KEYWORDS", "software engineer,intern,new grad,development program").split(",") if x.strip())

ANCHOR_RE = re.compile(r'<a\b(?=[^>]*\bhref=["\']([^"\']*/job/[^"\']+)["\'])(?=[^>]*\bdata-job-id=["\'](\d+)["\'])[^>]*>(.*?)</a>', re.I | re.S)
TITLE_RE = re.compile(r'<h2[^>]*>(.*?)</h2>', re.I | re.S)
LOCATION_RE = re.compile(r'class=["\']job-location["\'][^>]*>(.*?)</span>', re.I | re.S)
DATE_RE = re.compile(r'class=["\']job-date-posted["\'][^>]*>(.*?)</span>', re.I | re.S)

def _text(fragment):
    return clean(html.unescape(re.sub(r"<[^>]+>", " ", fragment)))

def scrape(token: str | None = None):
    page_url = token.strip() if token and token.strip() else CAREERS_URL
    parsed = urlsplit(page_url)
    base = f"{parsed.scheme or 'https'}://{parsed.netloc or 'jobs.dell.com'}"
    api_url = urljoin(base + "/", "search-jobs/results")
    headers = {**HEADERS, "Accept": "application/json, text/javascript, */*; q=0.01",
               "X-Requested-With": "XMLHttpRequest", "Referer": page_url}
    jobs = {}
    with requests.Session() as session:
        session.headers.update(headers)
        bootstrap = session.get(page_url, headers={**headers, "Accept": "text/html,application/xhtml+xml"}, timeout=TIMEOUT)
        bootstrap.raise_for_status()
        for keyword in KEYWORDS:
            for page in range(1, MAX_PAGES + 1):
                params = {
                    "ActiveFacetID": 0,
                    "CurrentPage": page,
                    "RecordsPerPage": PAGE_SIZE,
                    "Distance": 50,
                    "RadiusUnitType": 0,
                    "Keywords": keyword,
                    "Location": "",
                    "ShowRadius": "False",
                    "IsPagination": "False" if page == 1 else "True",
                    "SearchResultsModuleName": "Search Results",
                    "SearchFiltersModuleName": "Search Filters",
                    "SortCriteria": 0,
                    "SortDirection": 1,
                    "SearchType": 5,
                    "ResultsType": 0,
                }
                response = session.get(api_url, params=params, headers=headers, timeout=TIMEOUT)
                if not response.ok:
                    print(f"[Dell Technologies] Results endpoint returned HTTP {response.status_code}; parsing official search HTML")
                    fragment = bootstrap.text
                else:
                    try:
                        payload = response.json()
                        fragment = payload.get("results", "") if isinstance(payload, dict) else ""
                    except ValueError:
                        fragment = response.text
                if not fragment:
                    fragment = bootstrap.text
                matches = list(ANCHOR_RE.finditer(fragment or ""))
                added = 0
                for match in matches:
                    href, job_id, body = match.group(1), match.group(2), match.group(3)
                    title_match = TITLE_RE.search(body)
                    if not title_match or job_id in jobs:
                        continue
                    location_match = LOCATION_RE.search(body)
                    date_match = DATE_RE.search(body)
                    title = _text(title_match.group(1))
                    job_url = urljoin(base, href)
                    item = normalize(job_id, title, job_url,
                                     _text(location_match.group(1)) if location_match else None,
                                     None, None, None,
                                     _text(date_match.group(1)) if date_match else None,
                                     COMPANY_NAME, raw_payload={"keyword": keyword}, apply_url=job_url)
                    if item:
                        jobs[job_id] = item
                        added += 1
                print(f"[Dell Technologies] keyword={keyword!r} page={page}: {len(matches)} source rows, {added} new, {len(jobs)} unique")
                if added == 0 or len(matches) < PAGE_SIZE:
                    break
    if not jobs:
        raise RuntimeError("Dell Technologies official Radancy results endpoint returned no parseable listings")
    print(f"[Dell Technologies] Complete: {len(jobs)} jobs")
    return list(jobs.values())
