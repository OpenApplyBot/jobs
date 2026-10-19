"""LG Electronics global careers scraper using its public jobs JSON API."""
from __future__ import annotations

import os
import requests

from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "LG Electronics"
CAREERS_URL = "https://globalcareers.lge.com/jobs"
API_URL = "https://globalcareers.lge.com/api/job/v1/jobs/"
OFFICIAL_DOMAIN = "globalcareers.lge.com"
CSV_RANK = 20
PAGE_SIZE = max(1, min(100, int(os.getenv("LG_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("LG_MAX_PAGES", "12"))))

API_HEADERS = {
    **HEADERS,
    "Accept": "application/json, text/plain, */*",
    "Referer": CAREERS_URL,
    "Origin": "https://globalcareers.lge.com",
}

def _extract(payload):
    if not isinstance(payload, dict):
        return [], None
    node = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    rows = node.get("list") or node.get("jobs") or node.get("items") or node.get("content") or []
    total = node.get("total") or node.get("totalCount") or node.get("count")
    return (rows if isinstance(rows, list) else []), total

def scrape(token: str | None = None):
    output, seen = [], set()
    with requests.Session() as session:
        session.headers.update(API_HEADERS)
        for page in range(1, MAX_PAGES + 1):
            response = session.get(API_URL, params={"page": page, "size": PAGE_SIZE}, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            rows, total = _extract(payload)
            if not rows:
                if page == 1:
                    raise RuntimeError(f"LG official jobs API returned no rows; keys={list(payload)[:10]}")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict):
                    continue
                job_id = clean(row.get("id") or row.get("jobId") or row.get("externalId"))
                title = clean(row.get("title") or row.get("name"))
                if not job_id or not title or job_id in seen:
                    continue
                seen.add(job_id)
                job_url = clean(row.get("url") or row.get("jobUrl")) or f"https://globalcareers.lge.com/jobs/{job_id}"
                if job_url.startswith("/"):
                    job_url = "https://globalcareers.lge.com" + job_url
                location = row.get("location") or row.get("locations") or row.get("workLocation")
                if isinstance(location, (dict, list)):
                    location = location_text(location)
                description = clean(row.get("content") or row.get("description") or row.get("summary"))
                item = normalize(job_id, title, job_url, clean(location), clean(row.get("jobFamily") or row.get("department")),
                                 clean(row.get("employmentType") or row.get("jobType")), description,
                                 row.get("postedDate") or row.get("createdAt"), COMPANY_NAME,
                                 raw_payload=row, apply_url=job_url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[LG] Page {page}: {len(rows)} source rows, {added} new, {len(output)} total")
            if (total and page * PAGE_SIZE >= int(total)) or len(rows) < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("LG official jobs API returned no normalized listings")
    print(f"[LG] Complete: {len(output)} jobs")
    return output
