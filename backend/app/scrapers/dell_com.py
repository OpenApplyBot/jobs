"""Dell Technologies Careers scraper using its public jobs JSON API."""
from __future__ import annotations
import os
import requests
from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "Dell Technologies"
CAREERS_URL = "https://jobs.dell.com/en/search-jobs"
API_URL = "https://jobs.dell.com/api/job/v1/jobs/"
OFFICIAL_DOMAIN = "jobs.dell.com"
CSV_RANK = 30
PAGE_SIZE = max(1, min(100, int(os.getenv("DELL_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("DELL_MAX_PAGES", "2"))))

def _extract(payload):
    if not isinstance(payload, dict): return [], None
    node = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    rows = node.get("list") or node.get("jobs") or node.get("items") or []
    return (rows if isinstance(rows, list) else []), node.get("total") or node.get("totalCount") or node.get("count")

def scrape(token: str | None = None):
    output, seen = [], set()
    headers = {**HEADERS, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36", "Accept": "application/json, text/plain, */*", "Referer": CAREERS_URL, "Origin": "https://jobs.dell.com"}
    with requests.Session() as session:
        session.headers.update(headers)
        # Bootstrap a first-party session before querying the public jobs feed.
        session.get(CAREERS_URL, timeout=TIMEOUT)
        for page in range(1, MAX_PAGES + 1):
            response = session.get(API_URL, params={"page": page, "size": PAGE_SIZE}, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            rows, total = _extract(payload)
            if not rows:
                if page == 1: raise RuntimeError(f"Dell public jobs API returned no rows; keys={list(payload)[:10]}")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict): continue
                row = row.get("data") if isinstance(row.get("data"), dict) else row
                job_id = clean(row.get("id") or row.get("jobId") or row.get("jobSeqNo") or row.get("req_id"))
                title = clean(row.get("title") or row.get("name") or row.get("jobTitle"))
                if not job_id or not title or job_id in seen: continue
                seen.add(job_id)
                url = clean(row.get("url") or row.get("canonical_url") or row.get("applyUrl")) or f"https://jobs.dell.com/en/job/{job_id}"
                if url.startswith("/"): url = "https://jobs.dell.com" + url
                location = row.get("location") or row.get("locations") or row.get("full_location")
                if isinstance(location, (dict, list)): location = location_text(location)
                item = normalize(job_id, title, url, clean(location), clean(row.get("category") or row.get("department")), clean(row.get("employmentType") or row.get("jobType")), clean(row.get("description") or row.get("content")), row.get("postedDate") or row.get("posted_date"), COMPANY_NAME, raw_payload=row, apply_url=clean(row.get("applyUrl")) or url)
                if item: output.append(item); added += 1
            print(f"[Dell] Page {page}: {len(rows)} source rows, {added} new, {len(output)} total")
            if (total and page * PAGE_SIZE >= int(total)) or len(rows) < PAGE_SIZE: break
    if not output: raise RuntimeError("Dell public jobs API returned no normalized jobs")
    print(f"[Dell] Complete: {len(output)} jobs")
    return output
