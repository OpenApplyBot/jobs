"""Qualcomm Careers scraper using its public Eightfold jobs API."""
from __future__ import annotations

import os
import requests
from urllib.parse import urljoin

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Qualcomm"
CAREERS_URL = "https://careers.qualcomm.com/careers"
API_URL = "https://app.eightfold.ai/api/apply/v2/jobs"
OFFICIAL_DOMAIN = "qualcomm.com"
CSV_RANK = 29
PAGE_SIZE = max(1, min(100, int(os.getenv("QUALCOMM_PAGE_SIZE", "50"))))
MAX_PAGES = max(1, min(100, int(os.getenv("QUALCOMM_MAX_PAGES", "2"))))

API_HEADERS = {
    **HEADERS,
    "Accept": "application/json, text/plain, */*",
    "Referer": CAREERS_URL,
}

def scrape(token: str | None = None):
    output, seen = [], set()
    with requests.Session() as session:
        for page in range(MAX_PAGES):
            params = {"domain": "qualcomm.com", "num": PAGE_SIZE, "start": page * PAGE_SIZE}
            response = session.get(API_URL, params=params, headers=API_HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            rows = payload.get("positions") or payload.get("jobs") or payload.get("results") or []
            total = payload.get("count") or payload.get("total") or 0
            if not rows:
                if page == 0:
                    raise RuntimeError(f"Qualcomm Eightfold API returned no positions; keys={list(payload)[:10]}")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict):
                    continue
                job_id = clean(row.get("id") or row.get("job_id") or row.get("requisition_id"))
                title = clean(row.get("name") or row.get("title") or row.get("job_title"))
                if not job_id or not title or job_id in seen:
                    continue
                seen.add(job_id)
                raw_url = clean(row.get("canonicalPositionUrl") or row.get("url") or row.get("job_url"))
                job_url = urljoin("https://careers.qualcomm.com", raw_url) if raw_url else f"https://careers.qualcomm.com/careers/job/{job_id}"
                location = row.get("locations") or row.get("location")
                if isinstance(location, list):
                    location = ", ".join(clean(x.get("name") or x.get("city")) if isinstance(x, dict) else clean(x) for x in location if x)
                elif isinstance(location, dict):
                    location = location.get("name") or location.get("city")
                description = clean(row.get("job_description") or row.get("description") or row.get("summary"))
                item = normalize(job_id, title, job_url, clean(location),
                                 clean(row.get("department") or row.get("job_family") or row.get("category")),
                                 clean(row.get("employment_type") or row.get("job_type")), description,
                                 row.get("t_create") or row.get("posted_date"), COMPANY_NAME,
                                 raw_payload=row, apply_url=job_url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Qualcomm] Page {page + 1}: {len(rows)} source rows, {added} new, {len(output)} total of {total}")
            if (total and (page + 1) * PAGE_SIZE >= int(total)) or len(rows) < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Qualcomm official Eightfold API returned no normalized jobs")
    print(f"[Qualcomm] Complete: {len(output)} jobs")
    return output
