"""TikTok Careers scraper using the official public supplier search API."""
from __future__ import annotations

import os
import requests

from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "TikTok"
CAREERS_URL = "https://lifeattiktok.com/search?limit=12&offset=0"
API_URL = "https://api.lifeattiktok.com/api/v1/public/supplier/search/job/posts"
OFFICIAL_DOMAIN = "lifeattiktok.com"
CSV_RANK = 12
PAGE_SIZE = max(1, min(100, int(os.getenv("TIKTOK_PAGE_SIZE", "100"))))
MAX_PAGES = max(1, min(100, int(os.getenv("TIKTOK_MAX_PAGES", "30"))))

API_HEADERS = {
    **HEADERS,
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "website-path": "tiktok",
    "origin": "https://lifeattiktok.com",
    "referer": "https://lifeattiktok.com/",
}

def _extract_page(payload):
    if not isinstance(payload, dict):
        return [], None
    node = payload.get("data") or payload.get("result") or payload
    if not isinstance(node, dict):
        return [], None
    rows = node.get("job_post_list") or node.get("jobs") or node.get("list") or node.get("records") or []
    total = node.get("count") or node.get("total") or node.get("total_count")
    return (rows if isinstance(rows, list) else []), total

def scrape(token: str | None = None):
    """Return normalized public TikTok job records, paging through official search."""
    if token and token.strip():
        # Preserve compatibility for callers explicitly passing a public careers URL.
        page_url = token.strip()
        if page_url.startswith("https://lifeattiktok.com/"):
            response = requests.get(page_url, headers=API_HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            # If a caller passed a single detail/list URL, fall back to JSON-LD extraction.
            from .jsonld import scrape as scrape_jsonld
            rows = scrape_jsonld(page_url)
            if rows:
                return rows
    output, seen = [], set()
    with requests.Session() as session:
        for page in range(MAX_PAGES):
            offset = page * PAGE_SIZE
            payload = {
                "limit": PAGE_SIZE,
                "offset": offset,
                "keyword": "",
                "recruitment_id_list": ["202"],
                "category_id_list": [],
                "subject_id_list": [],
                "location_code_list": [],
                "job_function_id_list": [],
            }
            response = session.post(API_URL, json=payload, headers=API_HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            body = response.json()
            rows, total = _extract_page(body)
            if not rows:
                if page == 0:
                    raise RuntimeError(f"TikTok official API returned no job rows; response keys={list(body)[:12]}")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict):
                    continue
                post_info = row.get("job_post_info") or {}
                job_id = clean(row.get("code") or row.get("id") or row.get("job_id"))
                title = clean(row.get("title") or row.get("name") or row.get("job_title"))
                if not job_id or not title or job_id in seen:
                    continue
                seen.add(job_id)
                url = f"https://lifeattiktok.com/search/{job_id}"
                location = row.get("city_info") or row.get("location") or row.get("locations") or row.get("work_location")
                if isinstance(location, dict):
                    location = location.get("en_name") or location.get("name") or location.get("city_name") or location_text(location)
                elif isinstance(location, list):
                    location = ", ".join(str((v.get("en_name") or v.get("name") or v.get("city_name")) if isinstance(v, dict) else v) for v in location if v)
                category = row.get("job_category") or {}
                if isinstance(category, dict):
                    department = category.get("en_name") or category.get("name")
                else:
                    department = category
                recruit_type = row.get("recruit_type") or {}
                if isinstance(recruit_type, dict):
                    employment_type = recruit_type.get("en_name") or recruit_type.get("name")
                else:
                    employment_type = recruit_type
                description = "\n\n".join(filter(None, [clean(row.get("description")), clean(row.get("requirement"))]))
                posted_at = row.get("publish_time") or row.get("post_time") or row.get("create_time")
                item = normalize(job_id, title, url, clean(location), clean(department), clean(employment_type),
                                 description, posted_at, COMPANY_NAME, raw_payload=row, apply_url=url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[TikTok] Page {page + 1}: {len(rows)} source rows, {added} new, {len(output)} cumulative")
            if (total is not None and offset + len(rows) >= int(total)) or len(rows) < PAGE_SIZE:
                break
    print(f"[TikTok] Complete: {len(output)} jobs")
    return output
