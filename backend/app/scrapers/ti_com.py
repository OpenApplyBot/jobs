"""Texas Instruments scraper using the public Workday CXS jobs endpoint."""
from __future__ import annotations
import os
import requests
from urllib.parse import urljoin
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Texas Instruments"
CAREERS_URL = "https://ti.wd5.myworkdayjobs.com/en-US/TIjobs"
API_URL = "https://ti.wd5.myworkdayjobs.com/wday/cxs/ti/TIjobs/jobs"
OFFICIAL_DOMAIN = "ti.wd5.myworkdayjobs.com"
CSV_RANK = 37
PAGE_SIZE = max(1, min(100, int(os.getenv("TI_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("TI_MAX_PAGES", "2"))))

def scrape(token: str | None = None):
    output, seen = [], set()
    headers = {**HEADERS, "Accept": "application/json", "Content-Type": "application/json", "Origin": "https://ti.wd5.myworkdayjobs.com", "Referer": CAREERS_URL}
    with requests.Session() as session:
        for page in range(MAX_PAGES):
            body = {"limit": PAGE_SIZE, "offset": page * PAGE_SIZE, "searchText": "", "appliedFacets": {}}
            response = session.post(API_URL, json=body, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            rows = payload.get("jobPostings") or []
            total = payload.get("total")
            if not rows:
                if page == 0: raise RuntimeError(f"Texas Instruments Workday API returned no jobPostings; keys={list(payload)[:10]}")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict): continue
                external_path = clean(row.get("externalPath"))
                title = clean(row.get("title"))
                if not external_path or not title or external_path in seen: continue
                seen.add(external_path)
                url = urljoin("https://ti.wd5.myworkdayjobs.com/en-US/TIjobs/", external_path.lstrip("/"))
                item = normalize(external_path, title, url, clean(row.get("locationsText")), None, None, None, row.get("postedOn"), COMPANY_NAME, raw_payload=row, apply_url=url)
                if item: output.append(item); added += 1
            print(f"[TI] Page {page + 1}: {len(rows)} source rows, {added} new, {len(output)} total of {total}")
            if (total is not None and page * PAGE_SIZE + len(rows) >= int(total)) or len(rows) < PAGE_SIZE: break
    if not output: raise RuntimeError("Texas Instruments Workday API returned no normalized jobs")
    print(f"[TI] Complete: {len(output)} jobs")
    return output
