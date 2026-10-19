"""Baidu Careers scraper using its official public job-list endpoint."""
from __future__ import annotations

import os
import requests

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Baidu"
CAREERS_URL = "https://talent.baidu.com/jobs/list?recruitType=GRADUATE"
API_URL = "https://talent.baidu.com/httservice/getPostListNew"
OFFICIAL_DOMAIN = "talent.baidu.com"
CSV_RANK = 15
PAGE_SIZE = max(1, min(100, int(os.getenv("BAIDU_PAGE_SIZE", "100"))))
MAX_PAGES = max(1, min(100, int(os.getenv("BAIDU_MAX_PAGES", "20"))))
RECRUIT_TYPES = tuple(x.strip() for x in os.getenv("BAIDU_RECRUIT_TYPES", "GRADUATE,SOCIAL,INTERN").split(",") if x.strip())

API_HEADERS = {
    **HEADERS,
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://talent.baidu.com",
    "Referer": CAREERS_URL,
}

def _unwrap(payload):
    if not isinstance(payload, dict):
        return [], 0
    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    rows = data.get("list") or []
    if not rows and isinstance(data.get("listData"), dict):
        rows = data["listData"].get("listDetailData") or []
    total = data.get("total") or data.get("totalCount") or data.get("totalRows") or 0
    return (rows if isinstance(rows, list) else []), total

def scrape(token: str | None = None):
    if token and token.strip():
        from .auto import scrape as auto_scrape
        rows = auto_scrape(token.strip())
        if rows:
            return rows
    output, seen = [], set()
    with requests.Session() as session:
        session.headers.update(API_HEADERS)
        session.get(CAREERS_URL, timeout=TIMEOUT).raise_for_status()
        for recruit_type in RECRUIT_TYPES:
            for page in range(1, MAX_PAGES + 1):
                form = {
                    "recruitType": recruit_type,
                    "pageSize": PAGE_SIZE,
                    "curPage": page,
                    "projectType": "",
                    "keyWord": "",
                }
                response = session.post(API_URL, data=form, headers=API_HEADERS, timeout=TIMEOUT)
                response.raise_for_status()
                payload = response.json()
                rows, total = _unwrap(payload)
                if not rows:
                    if page == 1 and recruit_type == RECRUIT_TYPES[0]:
                        raise RuntimeError(f"Baidu official job API returned no rows; keys={list(payload)[:10]}")
                    break
                added = 0
                for row in rows:
                    if not isinstance(row, dict):
                        continue
                    job_id = clean(row.get("postId") or row.get("jobId") or row.get("id"))
                    title = clean(row.get("name") or row.get("postName") or row.get("title"))
                    if not job_id or not title or job_id in seen:
                        continue
                    seen.add(job_id)
                    url = f"https://talent.baidu.com/jobs/detail/{recruit_type}/{job_id}"
                    location = clean(row.get("workPlace") or row.get("workPlaceName") or row.get("location"))
                    department = clean(row.get("bgShortName") or row.get("orgName") or row.get("postTypeName") or row.get("serviceType"))
                    description = clean(row.get("workContent"))
                    requirement = clean(row.get("serviceCondition"))
                    if requirement:
                        description = "\n\n".join(filter(None, [description, "Requirements: " + requirement]))
                    item = normalize(job_id, title, url, location, department, recruit_type, description,
                                     row.get("publishDate") or row.get("updateDate"), COMPANY_NAME,
                                     raw_payload=row, apply_url=url)
                    if item:
                        output.append(item)
                        added += 1
                print(f"[Baidu] {recruit_type} page {page}: {len(rows)} source rows, {added} new, {len(output)} total")
                if (total and page * PAGE_SIZE >= int(total)) or len(rows) < PAGE_SIZE:
                    break
    if not output:
        raise RuntimeError("Baidu official public job API returned no normalized listings")
    print(f"[Baidu] Complete: {len(output)} jobs")
    return output
