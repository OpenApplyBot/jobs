"""Tencent Careers scraper using the public Tencent recruitment search API."""
from __future__ import annotations

import os
import time
from urllib.parse import urljoin

import requests

from .auto import scrape as _auto_scrape
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Tencent"
CAREERS_URL = "https://careers.tencent.com/en-us/search.html"
SEARCH_URL = "https://careers.tencent.com/tencentcareer/api/post/Query"
OFFICIAL_DOMAIN = "tencent.com"
CSV_RANK = 13
PAGE_SIZE = max(1, min(50, int(os.getenv("TENCENT_PAGE_SIZE", "10"))))
MAX_PAGES = max(1, min(100, int(os.getenv("TENCENT_MAX_PAGES", "30"))))


def _extract(payload):
    data = payload.get("Data") or payload.get("data") or {}
    if not isinstance(data, dict):
        return [], None
    rows = data.get("Posts") or data.get("posts") or data.get("jobList") or []
    total = data.get("Count") or data.get("count") or data.get("total")
    return rows if isinstance(rows, list) else [], total


def scrape(token: str | None = None):
    """Fetch public Tencent job listings with page-index pagination."""
    if token and token.strip():
        return _auto_scrape(token.strip())

    out, seen = [], set()
    headers = {
        **HEADERS,
        "Accept": "application/json, text/plain, */*",
        "Referer": CAREERS_URL,
    }
    try:
        with requests.Session() as session:
            for page in range(1, MAX_PAGES + 1):
                params = {
                    "timestamp": int(time.time() * 1000),
                    "countryId": "",
                    "cityId": "",
                    "bgIds": "",
                    "productId": "",
                    "categoryId": "",
                    "parentCategoryId": "",
                    "attrId": "",
                    "keyword": "",
                    "pageIndex": page,
                    "pageSize": PAGE_SIZE,
                    "language": "en-us",
                    "area": "us",
                }
                response = session.get(SEARCH_URL, params=params, headers=headers, timeout=TIMEOUT)
                response.raise_for_status()
                rows, total = _extract(response.json())
                if not rows:
                    break
                for row in rows:
                    if not isinstance(row, dict):
                        continue
                    job_id = row.get("PostId") or row.get("postId") or row.get("id")
                    title = clean(row.get("RecruitPostName") or row.get("recruitPostName") or row.get("title"))
                    if not job_id or not title or str(job_id) in seen:
                        continue
                    seen.add(str(job_id))
                    raw_url = row.get("PostURL") or row.get("postUrl") or row.get("url")
                    job_url = urljoin("https://careers.tencent.com/", str(raw_url or f"jobdesc.html?postId={job_id}"))
                    location = clean(row.get("LocationName") or row.get("locationName") or row.get("location"))
                    department = clean(row.get("BGName") or row.get("CategoryName") or row.get("department"))
                    description = clean(row.get("Responsibility") or row.get("Requirement") or row.get("description"))
                    item = normalize(
                        job_id, title, job_url, location, department,
                        row.get("RecruitPostTypeName") or row.get("employmentType"),
                        description,
                        row.get("LastUpdateTime") or row.get("UpdateTime"),
                        COMPANY_NAME,
                        raw_payload=row,
                        apply_url=job_url,
                    )
                    if item:
                        out.append(item)
                print(f"[Tencent] Page {page}: {len(rows)} source rows, {len(out)} unique jobs")
                if len(rows) < PAGE_SIZE:
                    break
                try:
                    if total is not None and len(out) >= int(total):
                        break
                except (TypeError, ValueError):
                    pass
        if out:
            return out
        print("[Tencent] API returned no normalized rows; trying official careers page")
    except (requests.RequestException, ValueError, TypeError) as exc:
        print(f"[Tencent] API unavailable ({type(exc).__name__}: {exc}); trying official careers page")
    return _auto_scrape(CAREERS_URL)
