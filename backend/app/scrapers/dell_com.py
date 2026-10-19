"""Dell Technologies scraper using its public Oracle Recruiting Cloud API."""
from __future__ import annotations
import os
import requests
from urllib.parse import urlencode
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Dell Technologies"
CAREERS_URL = "https://enterpriseplatform.dell.com/hcmUI/CandidateExperience/en/sites/careers/jobs"
API_URL = "https://enterpriseplatform.dell.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
OFFICIAL_DOMAIN = "enterpriseplatform.dell.com"
CSV_RANK = 30
PAGE_SIZE = max(1, min(100, int(os.getenv("DELL_PAGE_SIZE", "25"))))
MAX_PAGES = max(1, min(100, int(os.getenv("DELL_MAX_PAGES", "2"))))
SITE_NUMBER = "CX_1001"

def scrape(token: str | None = None):
    output, seen = [], set()
    headers = {**HEADERS, "Accept": "application/json", "Referer": CAREERS_URL}
    with requests.Session() as session:
        session.headers.update(headers)
        for page in range(MAX_PAGES):
            # Oracle HCM requires offset inside the finder expression.
            finder = f"findReqs;siteNumber={SITE_NUMBER},limit={PAGE_SIZE},offset={page * PAGE_SIZE},sortBy=POSTING_DATES_DESC"
            params = {"onlyData": "true", "expand": "requisitionList", "finder": finder}
            response = session.get(API_URL, params=params, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            items = payload.get("items") if isinstance(payload, dict) else None
            if not isinstance(items, list) or not items:
                if page == 0:
                    raise RuntimeError(f"Dell Oracle HCM API returned no items; payload keys={list(payload)[:10] if isinstance(payload, dict) else type(payload).__name__}")
                break
            total = items[0].get("TotalJobsCount") if isinstance(items[0], dict) else None
            reqs = []
            for item in items:
                if isinstance(item, dict):
                    reqs.extend(item.get("requisitionList") or [])
            added = 0
            for req in reqs:
                if not isinstance(req, dict):
                    continue
                job_id = clean(req.get("Id") or req.get("RequisitionId") or req.get("JobId"))
                title = clean(req.get("Title") or req.get("ExternalTitle"))
                if not job_id or not title or job_id in seen:
                    continue
                seen.add(job_id)
                url = f"https://enterpriseplatform.dell.com/hcmUI/CandidateExperience/en/sites/careers/job/{job_id}"
                location = clean(req.get("PrimaryLocation") or req.get("PrimaryLocationName") or req.get("Location"))
                description = clean(req.get("ShortDescriptionStr") or req.get("ExternalDescriptionStr") or req.get("Description"))
                department = clean(req.get("OrganizationName") or req.get("DepartmentName") or req.get("JobFamily"))
                posted = req.get("PostingStartDate") or req.get("PostingDate") or req.get("PostedDate")
                item = normalize(job_id, title, url, location, department, None, description, posted,
                                 COMPANY_NAME, raw_payload=req, apply_url=url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Dell Technologies] Page {page + 1}: {len(reqs)} source rows, {added} new, {len(output)} total of {total}")
            if total is not None and len(output) >= int(total):
                break
            if not reqs or len(reqs) < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Dell Oracle HCM API returned no normalized job listings")
    print(f"[Dell Technologies] Complete: {len(output)} jobs")
    return output
