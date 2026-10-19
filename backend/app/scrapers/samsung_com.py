"""Samsung Electronics scraper using its public Workday CXS API."""
from __future__ import annotations
import os
import requests
from urllib.parse import urljoin
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Samsung Electronics"
CAREERS_URL = "https://sec.wd3.myworkdayjobs.com/en-US/Samsung_Careers"
API_URL = "https://sec.wd3.myworkdayjobs.com/wday/cxs/sec/Samsung_Careers/jobs"
OFFICIAL_DOMAIN = "sec.wd3.myworkdayjobs.com"
CSV_RANK = 17
PAGE_SIZE = max(1, min(100, int(os.getenv("SAMSUNG_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("SAMSUNG_MAX_PAGES", "10"))))

def scrape(token: str | None = None):
    output, seen = [], set()
    headers = {**HEADERS, "Accept": "application/json", "Content-Type": "application/json",
               "Origin": "https://sec.wd3.myworkdayjobs.com", "Referer": CAREERS_URL}
    with requests.Session() as session:
        session.headers.update(headers)
        session.get(CAREERS_URL, timeout=TIMEOUT)
        for page in range(MAX_PAGES):
            body = {"limit": PAGE_SIZE, "offset": page * PAGE_SIZE, "searchText": "", "appliedFacets": {}}
            response = session.post(API_URL, json=body, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            rows = payload.get("jobPostings") or []
            total = payload.get("total")
            if not rows:
                if page == 0:
                    raise RuntimeError(f"Samsung Workday API returned no jobPostings; keys={list(payload)[:10]}")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict):
                    continue
                external_path = clean(row.get("externalPath"))
                title = clean(row.get("title"))
                if not external_path or not title or external_path in seen:
                    continue
                seen.add(external_path)
                url = urljoin(CAREERS_URL + "/", external_path.lstrip("/"))
                item = normalize(external_path, title, url, clean(row.get("locationsText")),
                                 clean(row.get("jobFamily")), None, None, row.get("postedOn"),
                                 COMPANY_NAME, raw_payload=row, apply_url=url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Samsung] Page {page + 1}: {len(rows)} source rows, {added} new, {len(output)} total of {total}")
            if (total is not None and page * PAGE_SIZE + len(rows) >= int(total)) or len(rows) < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Samsung Workday API returned no normalized jobs")
    print(f"[Samsung] Complete: {len(output)} jobs")
    return output
