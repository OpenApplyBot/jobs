"""Huawei Careers scraper using the official public recruitment endpoint."""
from __future__ import annotations

import os
import time
import requests

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Huawei"
PORTAL_ROOT = "https://career.huawei.com/reccampportal"
CAREERS_URL = PORTAL_ROOT + "/portal5/campus-recruitment.html"
API_BASE = "https://career.huawei.com/reccampportal/services/portal/portalpub/getJob/newHr/page"
OFFICIAL_DOMAIN = "huawei.com"
CSV_RANK = 16
PAGE_SIZE = max(1, min(100, int(os.getenv("HUAWEI_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("HUAWEI_MAX_PAGES", "20"))))

API_HEADERS = {
    **HEADERS,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": CAREERS_URL,
    "X-Requested-With": "XMLHttpRequest",
}

def _extract_rows(payload):
    if not isinstance(payload, dict):
        return [], 0
    rows = payload.get("result") or payload.get("data") or payload.get("list") or []
    if isinstance(rows, dict):
        rows = rows.get("result") or rows.get("list") or rows.get("records") or []
    page = payload.get("pageVO") or payload.get("data", {}).get("pageVO", {}) if isinstance(payload.get("data"), dict) else payload.get("pageVO", {})
    total_pages = page.get("totalPages") or page.get("totalPage") or 0 if isinstance(page, dict) else 0
    return (rows if isinstance(rows, list) else []), total_pages

def scrape(token: str | None = None):
    if token and token.strip():
        from .auto import scrape as auto_scrape
        rows = auto_scrape(token.strip())
        if rows:
            return rows
    output, seen = [], set()
    with requests.Session() as session:
        session.headers.update(API_HEADERS)
        session.get(PORTAL_ROOT + "/", timeout=TIMEOUT).raise_for_status()
        session.get(CAREERS_URL, timeout=TIMEOUT).raise_for_status()
        for page in range(1, MAX_PAGES + 1):
            params = {
                "curPage": page,
                "pageSize": PAGE_SIZE,
                "jobFamilyCode": "",
                "deptCode": "",
                "searchText": "",
                "language": "zh_CN",
                "orderBy": "ISS_STARTDATE_DESC_AND_IS_HOT_JOB",
                "jobType": "3",
                "reqTime": int(time.time() * 1000),
            }
            url = f"{API_BASE}/{PAGE_SIZE}/{page}"
            response = session.get(url, params=params, headers=API_HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            rows, total_pages = _extract_rows(payload)
            if not rows:
                if page == 1:
                    raise RuntimeError(f"Huawei official API returned no jobs; keys={list(payload)[:10]}")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict):
                    continue
                job_id = clean(row.get("advertisementsIntegrationId") or row.get("jobId") or row.get("positionId") or row.get("id"))
                title = clean(row.get("jobname") or row.get("nameCn") or row.get("jobName") or row.get("title"))
                if not job_id or not title or job_id in seen:
                    continue
                seen.add(job_id)
                detail_id = clean(row.get("jobId") or job_id)
                data_source = clean(row.get("dataSource")) or "1"
                job_url = f"https://career.huawei.com/reccampportal/portal5/campus-recruitment-detail.html?jobId={detail_id}&dataSource={data_source}"
                location = clean(row.get("jobArea") or row.get("jobAddress") or row.get("workLocation") or row.get("city"))
                department = clean(row.get("jobFamilyName") or row.get("jobClassName") or row.get("jobSubcategoryName") or row.get("deptNameEn") or row.get("deptName") or row.get("department"))
                description = clean(row.get("mainBusiness") or row.get("mostlyDuty") or row.get("jobDesc") or row.get("description") or row.get("responsibility"))
                requirement = clean(row.get("jobRequire") or row.get("demand") or row.get("requirement") or row.get("qualification"))
                if requirement:
                    description = "\n\n".join(filter(None, [description, "Requirements: " + requirement]))
                item = normalize(job_id, title, job_url, location, department, "Full-time", description,
                                 row.get("releaseDate") or row.get("creationDate"), COMPANY_NAME,
                                 raw_payload=row, apply_url=job_url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Huawei] Page {page}: {len(rows)} source rows, {added} new, {len(output)} total")
            if total_pages and page >= int(total_pages):
                break
            if len(rows) < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Huawei official public job API returned no normalized listings")
    print(f"[Huawei] Complete: {len(output)} jobs")
    return output
