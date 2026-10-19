"""Panasonic Careers scraper using the first-party Jibe jobs API."""
from __future__ import annotations

import json
import os
import re
import requests

from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "Panasonic"
CAREERS_URL = "https://careers.na.panasonic.com/corporate/jobs/locations/country/India"
API_URL = "https://careers.na.panasonic.com/api/jobs"
OFFICIAL_DOMAIN = "careers.na.panasonic.com"
CSV_RANK = 19
PAGE_SIZE = max(1, min(100, int(os.getenv("PANASONIC_PAGE_SIZE", "10"))))
MAX_PAGES = max(1, min(100, int(os.getenv("PANASONIC_MAX_PAGES", "20"))))

API_HEADERS = {
    **HEADERS,
    "Accept": "application/json, text/plain, */*",
    "Referer": CAREERS_URL,
    "Origin": "https://careers.na.panasonic.com",
}

def _search_config(html):
    match = re.search(r"window\.searchConfig\s*=\s*(\{[\s\S]*?\})\s*;", html, re.I)
    if not match:
        return {}
    try:
        value = json.loads(match.group(1))
        return value if isinstance(value, dict) else {}
    except (ValueError, TypeError):
        return {}

def _unwrap(payload):
    if not isinstance(payload, dict):
        return [], None
    rows = payload.get("jobs") or payload.get("data", {}).get("jobs") if isinstance(payload.get("data"), dict) else payload.get("jobs", [])
    total = payload.get("totalCount") or payload.get("total") or payload.get("count")
    return (rows if isinstance(rows, list) else []), total

def scrape(token: str | None = None):
    page_url = token.strip() if token and token.strip() else CAREERS_URL
    with requests.Session() as session:
        page = session.get(page_url, headers=API_HEADERS, timeout=TIMEOUT)
        page.raise_for_status()
        config = _search_config(page.text)
        query = dict(config.get("query") or {})
        query.setdefault("internal", "false")
        query.setdefault("allLangs", "true")
        query.setdefault("dedupeLang", "en-us|en-us")
        query.setdefault("separator", "|")
        query.setdefault("facetField", "tags1|tags2|tags3|tags4")
        context = config.get("contextSettings") or {"currentContext": "corporate"}
        route_path = config.get("path") or "/corporate/jobs/locations/country/India"
        output, seen = [], set()
        for page_no in range(1, MAX_PAGES + 1):
            params = {**query, "path": route_path, "page": page_no, "limit": PAGE_SIZE}
            response = session.get(API_URL, params=params, headers=API_HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            rows, total = _unwrap(payload)
            if not rows:
                if page_no == 1:
                    raise RuntimeError(f"Panasonic official jobs API returned no rows; keys={list(payload)[:10]}")
                break
            added = 0
            for raw_row in rows:
                if not isinstance(raw_row, dict):
                    continue
                row = raw_row.get("data") if isinstance(raw_row.get("data"), dict) else raw_row
                job_id = clean(row.get("req_id") or row.get("slug") or row.get("id") or row.get("jobId"))
                title = clean(row.get("title") or row.get("name"))
                if not job_id or not title or job_id in seen:
                    continue
                seen.add(job_id)
                url = clean(row.get("canonical_url") or row.get("url") or row.get("apply_url"))
                if not url:
                    url = f"https://careers.na.panasonic.com/jobs/{job_id}?lang=en-us"
                if url.startswith("/"):
                    url = "https://careers.na.panasonic.com" + url
                location = clean(row.get("full_location") or row.get("location_name") or row.get("location"))
                if not location:
                    location = location_text([row.get("city"), row.get("state"), row.get("country")])
                category = row.get("categories") or row.get("category") or row.get("jobFamily")
                if isinstance(category, list):
                    category = ", ".join(clean(x.get("name") if isinstance(x, dict) else x) for x in category if x)
                elif isinstance(category, dict):
                    category = category.get("name") or category.get("title")
                item = normalize(job_id, title, url, location, clean(category),
                                 clean(row.get("employment_type") or row.get("tags1")),
                                 clean(row.get("description") or row.get("responsibilities")),
                                 row.get("posted_date") or row.get("created_at"), COMPANY_NAME,
                                 raw_payload=raw_row, apply_url=clean(row.get("apply_url")) or url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Panasonic] Page {page_no}: {len(rows)} source rows, {added} new, {len(output)} total")
            if (total and page_no * PAGE_SIZE >= int(total)) or len(rows) < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Panasonic official jobs API returned no normalized listings")
    print(f"[Panasonic] Complete: {len(output)} jobs")
    return output
