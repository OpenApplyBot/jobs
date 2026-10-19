"""Applied Materials scraper using its official Workday CXS endpoint."""
from __future__ import annotations
import os
import requests
from urllib.parse import urljoin
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Applied Materials"
CAREERS_URL = "https://amat.wd1.myworkdayjobs.com/en-US/External"
API_URL = "https://amat.wd1.myworkdayjobs.com/wday/cxs/amat/External/jobs"
OFFICIAL_DOMAIN = "amat.wd1.myworkdayjobs.com"
CSV_RANK = 38
PAGE_SIZE = max(1, min(100, int(os.getenv("APPLIED_MATERIALS_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("APPLIED_MATERIALS_MAX_PAGES", "2"))))

def scrape(token: str | None = None):
    output, seen = [], set()
    headers = {**HEADERS, "Accept": "application/json", "Content-Type": "application/json", "Origin": "https://amat.wd1.myworkdayjobs.com", "Referer": CAREERS_URL}
    with requests.Session() as session:
        for page in range(MAX_PAGES):
            body = {"limit": PAGE_SIZE, "offset": page * PAGE_SIZE, "searchText": "", "appliedFacets": {}}
            response = session.post(API_URL, json=body, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            rows = payload.get("jobPostings") or []
            total = payload.get("total")
            if not rows:
                if page == 0: raise RuntimeError(f"Applied Materials Workday API returned no jobPostings; keys={list(payload)[:10]}")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict): continue
                job_id = clean(row.get("externalPath") or row.get("jobReqId") or row.get("id"))
                title = clean(row.get("title"))
                if not job_id or not title or job_id in seen: continue
                seen.add(job_id)
                url = urljoin("https://amat.wd1.myworkdayjobs.com", "/en-US/External/" + job_id.lstrip("/"))
                location = clean(row.get("locationsText") or row.get("location"))
                posted = row.get("postedOn")
                item = normalize(job_id, title, url, location, clean(row.get("jobFamily") or row.get("category")), None, None, posted, COMPANY_NAME, raw_payload=row, apply_url=url)
                if item: output.append(item); added += 1
            print(f"[Applied Materials] Page {page + 1}: {len(rows)} source rows, {added} new, {len(output)} total of {total}")
            if (total is not None and page * PAGE_SIZE + len(rows) >= int(total)) or len(rows) < PAGE_SIZE: break
    if not output: raise RuntimeError("Applied Materials Workday API returned no normalized jobs")
    print(f"[Applied Materials] Complete: {len(output)} jobs")
    return output
