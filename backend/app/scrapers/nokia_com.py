"""Nokia Careers scraper using its public Oracle Recruiting Cloud API."""
from __future__ import annotations
import os
import requests
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Nokia"
CAREERS_URL = "https://fa-evmr-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1"
API_URL = "https://fa-evmr-saasfaprod1.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
SITE_NUMBER = os.getenv("NOKIA_SITE_NUMBER", "CX_1")
OFFICIAL_DOMAIN = "nokia.com"
CSV_RANK = 44
PAGE_SIZE = max(1, min(100, int(os.getenv("NOKIA_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("NOKIA_MAX_PAGES", "2"))))

def scrape(token: str | None = None):
    output, seen = [], set()
    headers = {**HEADERS, "Accept": "application/json", "Referer": CAREERS_URL}
    with requests.Session() as session:
        for page in range(MAX_PAGES):
            offset = page * PAGE_SIZE
            finder = f"findReqs;siteNumber={SITE_NUMBER},limit={PAGE_SIZE},offset={offset},sortBy=POSTING_DATES_DESC"
            response = session.get(API_URL, params={"onlyData": "true", "expand": "requisitionList", "finder": finder}, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            items = payload.get("items") or []
            if not items:
                if page == 0: raise RuntimeError(f"Nokia Oracle recruiting API returned no items; keys={list(payload)[:10]}")
                break
            container = items[0]
            rows = container.get("requisitionList") or []
            total = container.get("TotalJobsCount") or 0
            if not rows:
                if page == 0: raise RuntimeError("Nokia Oracle recruiting API returned no requisitions")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict): continue
                job_id = clean(row.get("Id") or row.get("RequisitionNumber") or row.get("JobId"))
                title = clean(row.get("Title") or row.get("JobTitle"))
                if not job_id or not title or job_id in seen: continue
                seen.add(job_id)
                url = f"https://fa-evmr-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/{SITE_NUMBER}/job/{job_id}"
                location = clean(row.get("PrimaryLocation") or row.get("Location") or row.get("WorkLocation"))
                description = clean(row.get("ExternalDescriptionStr") or row.get("ExternalResponsibilitiesStr"))
                item = normalize(job_id, title, url, location, clean(row.get("JobFamily") or row.get("Organization")), clean(row.get("JobType")), description, row.get("PostedDate"), COMPANY_NAME, raw_payload=row, apply_url=url)
                if item: output.append(item); added += 1
            print(f"[Nokia] Page {page + 1}: {len(rows)} source rows, {added} new, {len(output)} total of {total}")
            if (total and offset + len(rows) >= int(total)) or len(rows) < PAGE_SIZE: break
    if not output: raise RuntimeError("Nokia Oracle recruiting API returned no normalized jobs")
    print(f"[Nokia] Complete: {len(output)} jobs")
    return output
