"""ByteDance Global Careers scraper using the public supplier search API."""
from __future__ import annotations
import os
import requests
from .auto import scrape as _auto_scrape
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "ByteDance"
CAREERS_URL = "https://joinbytedance.com/search"
SEARCH_URL = "https://jobs.bytedance.com/api/v1/public/supplier/search/job/posts"
OFFICIAL_DOMAIN = "bytedance.com"
CSV_RANK = 11
PAGE_SIZE = max(1, min(100, int(os.getenv("BYTEDANCE_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("BYTEDANCE_MAX_PAGES", "30"))))

def _extract(payload):
    data = payload.get("data") or {}
    if not isinstance(data, dict):
        return [], None
    rows = data.get("job_post_list") or data.get("jobPostList") or data.get("jobs") or []
    return (rows if isinstance(rows, list) else []), data.get("count") or data.get("total")

def scrape(token: str | None = None):
    if token and token.strip():
        return _auto_scrape(token.strip())
    out, seen = [], set()
    headers = {
        **HEADERS,
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://joinbytedance.com",
        "Referer": CAREERS_URL,
        "portal-channel": "global",
        "portal-platform": "pc",
        "website-path": "global",
    }
    try:
        with requests.Session() as session:
            for page in range(MAX_PAGES):
                body = {
                    "keyword": "",
                    "limit": PAGE_SIZE,
                    "offset": page * PAGE_SIZE,
                    "portal_type": 3,
                    "portal_entrance": 1,
                    "language": "en",
                    "recruitment_id_list": [],
                    "job_category_id_list": [],
                    "location_code_list": [],
                    "subject_id_list": [],
                    "tag_id_list": [],
                    "storefront_id_list": [],
                    "job_function_id_list": [],
                }
                response = session.post(SEARCH_URL, json=body, headers=headers, timeout=TIMEOUT)
                response.raise_for_status()
                payload = response.json()
                if payload.get("code") not in (None, 0, "0"):
                    raise ValueError(f"ByteDance API returned code {payload.get('code')}: {payload.get('message')}")
                rows, total = _extract(payload)
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
                    location = row.get("city_info") or row.get("city_list") or row.get("city") or row.get("location")
                    if isinstance(location, dict):
                        location = location.get("en_name") or location.get("name") or location.get("city_name")
                    elif isinstance(location, list):
                        location = ", ".join(clean(x.get("en_name") or x.get("name")) if isinstance(x, dict) else clean(x) for x in location if x)
                    job_url = clean(row.get("url") or row.get("job_url")) or f"https://joinbytedance.com/search/{job_id}"
                    category = row.get("job_category")
                    if isinstance(category, dict):
                        category = category.get("en_name") or category.get("name")
                    item = normalize(
                        job_id, title, job_url, clean(location),
                        clean(category or row.get("job_function")),
                        row.get("employment_type") or row.get("employmentType"),
                        row.get("description") or row.get("requirement"),
                        row.get("publish_time") or row.get("create_time") or row.get("update_time"),
                        COMPANY_NAME, raw_payload=row, apply_url=job_url,
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
            print(f"[ByteDance] Complete: {len(out)} jobs")
            return out
        raise ValueError("Public supplier API returned no normalized jobs")
    except (requests.RequestException, ValueError, TypeError) as exc:
        print(f"[ByteDance] Global public API unavailable ({type(exc).__name__}: {exc}); trying official page")
        return _auto_scrape(CAREERS_URL)
