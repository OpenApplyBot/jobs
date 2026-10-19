"""ByteDance Careers scraper using its public job-search API.

The public careers search endpoint is queried page-by-page. If its response
contract changes, the scraper falls back to the official public careers page.
"""
from __future__ import annotations

import os
import requests

from .auto import scrape as _auto_scrape
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "ByteDance"
CAREERS_URL = "https://joinbytedance.com/search"
SEARCH_URL = "https://jobs.bytedance.com/api/v1/search/job/posts"
OFFICIAL_DOMAIN = "bytedance.com"
CSV_RANK = 11
PAGE_SIZE = max(1, min(50, int(os.getenv("BYTEDANCE_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("BYTEDANCE_MAX_PAGES", "30"))))


def _extract(payload):
    data = payload.get("data") or {}
    if not isinstance(data, dict):
        return [], None
    rows = data.get("job_post_list") or data.get("jobPostList") or data.get("jobs") or []
    total = data.get("count") or data.get("total") or data.get("total_count")
    return rows if isinstance(rows, list) else [], total


def scrape(token: str | None = None):
    """Fetch ByteDance listings from its public API with a bounded page limit."""
    if token and token.strip():
        return _auto_scrape(token.strip())

    out, seen = [], set()
    headers = {
        **HEADERS,
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://jobs.bytedance.com",
        "Referer": "https://jobs.bytedance.com/en/position",
    }
    try:
        with requests.Session() as session:
            for page in range(MAX_PAGES):
                offset = page * PAGE_SIZE
                body = {
                    "keyword": "",
                    "limit": PAGE_SIZE,
                    "offset": offset,
                    "job_category": "",
                    "job_function": "",
                    "city": "",
                    "portal_type": 1,
                    "recruitment_id": "",
                    "subject_id": "",
                    "language_code": 2,
                }
                response = session.post(SEARCH_URL, json=body, headers=headers, timeout=TIMEOUT)
                response.raise_for_status()
                rows, total = _extract(response.json())
                if not rows:
                    break
                for row in rows:
                    if not isinstance(row, dict):
                        continue
                    job_id = row.get("id") or row.get("job_post_id") or row.get("jobPostId")
                    title = clean(row.get("title") or row.get("position_name") or row.get("job_title"))
                    if not job_id or not title or str(job_id) in seen:
                        continue
                    seen.add(str(job_id))
                    locations = row.get("city_info") or row.get("city") or row.get("location")
                    if isinstance(locations, dict):
                        locations = locations.get("name") or locations.get("city_name") or locations
                    job_url = clean(row.get("url") or row.get("job_url"))
                    if not job_url:
                        job_url = f"https://jobs.bytedance.com/en/position/{job_id}"
                    item = normalize(
                        job_id,
                        title,
                        job_url,
                        clean(locations),
                        clean(row.get("job_category") or row.get("job_function") or row.get("department")),
                        row.get("employment_type") or row.get("employmentType"),
                        row.get("description") or row.get("description_text"),
                        row.get("publish_time") or row.get("create_time") or row.get("update_time"),
                        COMPANY_NAME,
                        raw_payload=row,
                        apply_url=job_url,
                    )
                    if item:
                        out.append(item)
                print(f"[ByteDance] Page {page + 1}: {len(rows)} source rows, {len(out)} unique jobs")
                if len(rows) < PAGE_SIZE:
                    break
                try:
                    if total is not None and len(out) >= int(total):
                        break
                except (TypeError, ValueError):
                    pass
        if out:
            return out
        print("[ByteDance] Public API returned no normalized rows; trying official careers page")
    except (requests.RequestException, ValueError, TypeError) as exc:
        print(f"[ByteDance] Public API unavailable ({type(exc).__name__}: {exc}); trying official careers page")
    return _auto_scrape(CAREERS_URL)
