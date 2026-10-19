"""Salesforce Careers scraper using its public Workday CXS jobs API."""
from __future__ import annotations
import os
import time
import requests
from urllib.parse import urljoin
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Salesforce"
CAREERS_URL = "https://salesforce.wd12.myworkdayjobs.com/en-US/External_Career_Site"
API_URL = "https://salesforce.wd12.myworkdayjobs.com/wday/cxs/salesforce/External_Career_Site/jobs"
OFFICIAL_DOMAIN = "salesforce.wd12.myworkdayjobs.com"
CSV_RANK = 23
PAGE_SIZE = max(1, min(100, int(os.getenv("SALESFORCE_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("SALESFORCE_MAX_PAGES", "2"))))

def scrape(token: str | None = None):
    output, seen = [], set()
    headers = {**HEADERS, "Accept": "application/json", "Content-Type": "application/json",
               "Origin": "https://salesforce.wd12.myworkdayjobs.com", "Referer": CAREERS_URL}
    with requests.Session() as session:
        session.headers.update(headers)
        # Bootstrap the official career site for session/cookies.
        session.get(CAREERS_URL, timeout=TIMEOUT)
        for page in range(MAX_PAGES):
            body = {"limit": PAGE_SIZE, "offset": page * PAGE_SIZE, "searchText": "", "appliedFacets": {}}
            response = None
            for attempt in range(6):
                response = session.post(API_URL, json=body, headers=headers, timeout=TIMEOUT)
                if response.status_code != 429:
                    break
                if output:
                    print(f"[Salesforce] Rate limited after {len(output)} valid listings; returning collected records")
                    break
                wait = response.headers.get("Retry-After")
                try:
                    delay = min(60, max(1, int(wait))) if wait else min(60, 2 ** attempt)
                except ValueError:
                    delay = min(60, 2 ** attempt)
                print(f"[Salesforce] First-page rate limit; retry {attempt + 1}/6 after {delay}s")
                time.sleep(delay)
            if response is None:
                raise RuntimeError("Salesforce Workday API did not return a response")
            if response.status_code == 429 and output:
                break
            response.raise_for_status()
            payload = response.json()
            rows = payload.get("jobPostings") or []
            total = payload.get("total")
            if not rows:
                if page == 0:
                    raise RuntimeError(f"Salesforce Workday API returned no jobPostings; keys={list(payload)[:10]}")
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
            print(f"[Salesforce] Page {page + 1}: {len(rows)} source rows, {added} new, {len(output)} total of {total}")
            if (total is not None and (page * PAGE_SIZE + len(rows)) >= int(total)) or len(rows) < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Salesforce Workday API returned no normalized jobs")
    print(f"[Salesforce] Complete: {len(output)} jobs")
    return output
