"""Oracle Careers scraper using the public Oracle Recruiting Cloud API."""
from __future__ import annotations

import os
import requests
from urllib.parse import quote

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Oracle"
CAREERS_URL = "https://careers.oracle.com/en/sites/jobsearch/"
API_URL = "https://eeho.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
SITE_NUMBER = os.getenv("ORACLE_SITE_NUMBER", "CX_45001")
OFFICIAL_DOMAIN = "oracle.com"
CSV_RANK = 22
PAGE_SIZE = max(1, min(200, int(os.getenv("ORACLE_PAGE_SIZE", "50"))))
MAX_PAGES = max(1, min(100, int(os.getenv("ORACLE_MAX_PAGES", "2"))))

def _finder(offset):
    return f"findReqs;siteNumber={SITE_NUMBER},limit={PAGE_SIZE},offset={offset},sortBy=POSTING_DATES_DESC"

def scrape(token: str | None = None):
    output, seen = [], set()
    with requests.Session() as session:
        session.headers.update({**HEADERS, "Accept": "application/json", "Referer": CAREERS_URL})
        for page in range(MAX_PAGES):
            offset = page * PAGE_SIZE
            params = {"onlyData": "true", "expand": "requisitionList", "finder": _finder(offset)}
            response = session.get(API_URL, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            items = payload.get("items") or []
            if not items:
                if page == 0:
                    raise RuntimeError(f"Oracle public recruiting API returned no items; keys={list(payload)[:10]}")
                break
            container = items[0]
            rows = container.get("requisitionList") or []
            total = container.get("TotalJobsCount") or 0
            if not rows:
                if page == 0:
                    raise RuntimeError("Oracle public recruiting API returned no requisitions")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict):
                    continue
                job_id = clean(row.get("Id") or row.get("RequisitionNumber") or row.get("JobId"))
                title = clean(row.get("Title") or row.get("JobTitle"))
                if not job_id or not title or job_id in seen:
                    continue
                seen.add(job_id)
                job_url = f"https://careers.oracle.com/jobs/#en/sites/jobsearch/job/{job_id}"
                location = clean(row.get("PrimaryLocation") or row.get("Location") or row.get("WorkLocation"))
                department = clean(row.get("JobFamily") or row.get("Organization") or row.get("Category"))
                description = clean(row.get("ExternalDescriptionStr") or row.get("ExternalResponsibilitiesStr"))
                item = normalize(job_id, title, job_url, location, department, clean(row.get("JobType")),
                                 description, row.get("PostedDate"), COMPANY_NAME,
                                 raw_payload=row, apply_url=job_url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Oracle] Page {page + 1}: {len(rows)} source rows, {added} new, {len(output)} total of {total}")
            if (total and offset + len(rows) >= int(total)) or len(rows) < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Oracle public recruiting API returned no normalized jobs")
    print(f"[Oracle] Complete: {len(output)} jobs")
    return output
