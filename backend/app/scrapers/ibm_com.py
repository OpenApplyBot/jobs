"""IBM Careers scraper using IBM's public Genesis search API."""
from __future__ import annotations

import os
import requests
from urllib.parse import urljoin

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "IBM"
CAREERS_URL = "https://www.ibm.com/careers/search"
API_URL = "https://www-api.ibm.com/search/api/v2"
OFFICIAL_DOMAIN = "ibm.com"
CSV_RANK = 21
PAGE_SIZE = max(1, min(100, int(os.getenv("IBM_PAGE_SIZE", "100"))))
MAX_PAGES = max(1, min(100, int(os.getenv("IBM_MAX_PAGES", "20"))))

API_HEADERS = {
    **HEADERS,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://www.ibm.com",
    "Referer": CAREERS_URL,
}

def _total_value(value):
    if isinstance(value, dict):
        return value.get("value", 0)
    return value or 0

def scrape(token: str | None = None):
    output, seen = [], set()
    query = {"bool": {"must": [{"simple_query_string": {"query": "*"}}]}}
    fields = ["url", "title", "description", "country", "region", "category"]
    with requests.Session() as session:
        for page in range(MAX_PAGES):
            body = {
                "appId": "careers",
                "scopes": ["careers2"],
                "query": query,
                "size": PAGE_SIZE,
                "from": page * PAGE_SIZE,
                "_source": fields,
            }
            response = session.post(API_URL, json=body, headers=API_HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            hits_block = payload.get("hits") or {}
            hits = hits_block.get("hits") or []
            total = _total_value(hits_block.get("total"))
            if not hits:
                if page == 0:
                    raise RuntimeError(f"IBM public careers API returned no hits; keys={list(payload)[:10]}")
                break
            added = 0
            for hit in hits:
                if not isinstance(hit, dict):
                    continue
                row = hit.get("_source") or {}
                job_id = clean(hit.get("_id") or row.get("job_id") or row.get("id"))
                title = clean(row.get("title") or row.get("name"))
                raw_url = clean(row.get("url") or row.get("apply_url"))
                if not job_id or not title or not raw_url or job_id in seen:
                    continue
                seen.add(job_id)
                job_url = urljoin("https://www.ibm.com", raw_url)
                country = row.get("country") or []
                if isinstance(country, list):
                    country = ", ".join(clean(x) for x in country if x)
                location = ", ".join(filter(None, [clean(row.get("region")), clean(country)]))
                item = normalize(job_id, title, job_url, location, clean(row.get("category")), None,
                                 row.get("description"), None, COMPANY_NAME, raw_payload=row, apply_url=job_url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[IBM] Page {page + 1}: {len(hits)} source rows, {added} new, {len(output)} total of {total}")
            if page * PAGE_SIZE + len(hits) >= int(total or 0) or len(hits) < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("IBM public careers API returned no normalized listings")
    print(f"[IBM] Complete: {len(output)} jobs")
    return output
