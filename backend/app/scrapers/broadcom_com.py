"""Broadcom scraper probing known public Workday board IDs in order."""
from __future__ import annotations
import os
import requests
from urllib.parse import urljoin
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Broadcom"
OFFICIAL_DOMAIN = "broadcom.com"
CSV_RANK = 35
PAGE_SIZE = max(1, min(100, int(os.getenv("BROADCOM_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("BROADCOM_MAX_PAGES", "2"))))
BOARDS = tuple(x.strip() for x in os.getenv("BROADCOM_WORKDAY_BOARDS", "External_Career,External,BroadcomCareers,BCICareers").split(",") if x.strip())

def scrape(token: str | None = None):
    headers = {**HEADERS, "Accept": "application/json", "Content-Type": "application/json", "Origin": "https://broadcom.wd1.myworkdayjobs.com"}
    with requests.Session() as session:
        chosen = None
        first_error = None
        for board in BOARDS:
            base = f"https://broadcom.wd1.myworkdayjobs.com/{board}"
            api = f"https://broadcom.wd1.myworkdayjobs.com/wday/cxs/broadcom/{board}/jobs"
            try:
                response = session.post(api, json={"limit": PAGE_SIZE, "offset": 0, "searchText": "", "appliedFacets": {}}, headers={**headers, "Referer": base}, timeout=TIMEOUT)
                if response.status_code in (404, 410):
                    continue
                response.raise_for_status()
                payload = response.json()
                if isinstance(payload.get("jobPostings"), list) and payload["jobPostings"]:
                    chosen = (board, base, api, payload)
                    break
            except (requests.RequestException, ValueError) as exc:
                first_error = first_error or exc
                continue
        if not chosen:
            if first_error:
                raise RuntimeError(f"Broadcom public Workday board discovery found no usable board; first error: {type(first_error).__name__}: {first_error}") from first_error
            raise RuntimeError(f"Broadcom public Workday board discovery found no postings in candidates: {', '.join(BOARDS)}")
        board, base, api, first_payload = chosen
        print(f"[Broadcom] Verified public Workday board ID: {board}")
        output, seen = [], set()
        for page in range(MAX_PAGES):
            if page == 0:
                payload = first_payload
            else:
                response = session.post(api, json={"limit": PAGE_SIZE, "offset": page * PAGE_SIZE, "searchText": "", "appliedFacets": {}}, headers={**headers, "Referer": base}, timeout=TIMEOUT)
                response.raise_for_status()
                payload = response.json()
            rows = payload.get("jobPostings") or []
            total = payload.get("total")
            if not rows:
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict): continue
                external_path = clean(row.get("externalPath"))
                title = clean(row.get("title"))
                if not external_path or not title or external_path in seen: continue
                seen.add(external_path)
                url = urljoin(base + "/", external_path.lstrip("/"))
                item = normalize(external_path, title, url, clean(row.get("locationsText")), None, None, None, row.get("postedOn"), COMPANY_NAME, raw_payload=row, apply_url=url)
                if item: output.append(item); added += 1
            print(f"[Broadcom] Page {page + 1}: {len(rows)} source rows, {added} new, {len(output)} total of {total}")
            if (total is not None and page * PAGE_SIZE + len(rows) >= int(total)) or len(rows) < PAGE_SIZE: break
    if not output: raise RuntimeError("Broadcom public Workday API returned no normalized jobs")
    print(f"[Broadcom] Complete: {len(output)} jobs")
    return output
