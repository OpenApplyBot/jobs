"""Alibaba Group Careers scraper using its public position search API."""
from __future__ import annotations

import os
import re
import uuid
import requests

from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "Alibaba Group"
CAREERS_URL = "https://talent.alibaba.com/off-campus/position-list?lang=zh"
API_URL = "https://talent.alibaba.com/position/search"
OFFICIAL_DOMAIN = "talent.alibaba.com"
CSV_RANK = 14
PAGE_SIZE = max(1, min(100, int(os.getenv("ALIBABA_PAGE_SIZE", "50"))))
MAX_PAGES = max(1, min(100, int(os.getenv("ALIBABA_MAX_PAGES", "20"))))
CHANNEL = os.getenv("ALIBABA_CHANNEL", "group_official_site")

API_HEADERS = {
    **HEADERS,
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
    "origin": "https://talent.alibaba.com",
    "referer": CAREERS_URL,
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8",
}

def _unwrap(payload):
    """Handle current and legacy envelopes returned by Alibaba's recruiting API."""
    if not isinstance(payload, dict):
        return [], None
    node = payload.get("content") if isinstance(payload.get("content"), dict) else payload
    if not isinstance(node, dict):
        node = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    rows = []
    for key in ("datas", "records", "list", "positions", "items", "rows"):
        if isinstance(node.get(key), list):
            rows = node[key]
            break
    total = node.get("totalCount") or node.get("total") or node.get("totalSize") or node.get("count")
    if not rows and isinstance(payload.get("data"), list):
        rows = payload["data"]
    return rows, total

def scrape(token: str | None = None):
    """Fetch paginated public jobs and normalize to OpenApplyBot's canonical schema."""
    if token and token.strip():
        page_url = token.strip()
        if page_url.startswith("https://talent.alibaba.com/"):
            from .jsonld import scrape as scrape_jsonld
            rows = scrape_jsonld(page_url)
            if rows:
                return rows
    output, seen = [], set()
    # The public endpoint uses a double-submit CSRF check: the same
    # anonymous token is sent in the cookie and header. No login is required.
    csrf = str(uuid.uuid4())
    with requests.Session() as session:
        session.headers.update({
            **API_HEADERS,
            "cookie": f"XSRF-TOKEN={csrf}",
            "x-xsrf-token": csrf,
        })
        for page in range(1, MAX_PAGES + 1):
            payload = {
                "channel": CHANNEL,
                "language": "zh",
                "batchId": "",
                "categories": "",
                "deptCodes": [],
                "key": "",
                "pageIndex": page,
                "pageSize": PAGE_SIZE,
                "regions": "",
                "subCategories": "",
            }
            response = session.post(API_URL, json=payload, headers={
                **API_HEADERS,
                "cookie": f"XSRF-TOKEN={csrf}",
                "x-xsrf-token": csrf,
            }, timeout=TIMEOUT)
            response.raise_for_status()
            body = response.json()
            if body.get("success") is False:
                raise RuntimeError(f"Alibaba public position API reported failure: {body.get('errorMsg') or body.get('errorCode') or 'success=false'}")
            rows, total = _unwrap(body)
            if not rows:
                if page == 1:
                    raise RuntimeError(f"Alibaba public position API returned no records; top-level keys={list(body)[:12]}, content keys={list(body.get('content', {}))[:12] if isinstance(body.get('content'), dict) else []}")
                break
            added = 0
            for row in rows:
                if not isinstance(row, dict):
                    continue
                job_id = clean(row.get("id") or row.get("positionId") or row.get("code") or row.get("jobId"))
                title = clean(row.get("name") or row.get("positionName") or row.get("title"))
                if not job_id or not title or job_id in seen:
                    continue
                seen.add(job_id)
                url = f"https://talent.alibaba.com/off-campus/position-detail?positionId={job_id}"
                locations = row.get("workLocations") or row.get("workLocation") or row.get("location") or row.get("city")
                if isinstance(locations, list):
                    location = ", ".join(clean(v.get("name") or v.get("cityName") or v.get("enName") or v.get("city")) if isinstance(v, dict) else clean(v) for v in locations if v)
                elif isinstance(locations, dict):
                    location = locations.get("name") or locations.get("cityName") or locations.get("enName") or location_text(locations)
                else:
                    location = clean(locations)
                department = row.get("deptName") or row.get("departmentName") or row.get("department") or row.get("buName") or row.get("categories")
                if isinstance(department, list):
                    department = ", ".join(clean(x) for x in department if x)
                description = clean(row.get("description") or row.get("jobDescription"))
                requirement = clean(row.get("requirement") or row.get("requirements"))
                if requirement:
                    description = "\\n\\n".join(filter(None, [description, "Requirements: " + requirement]))
                posted_at = row.get("publishTime") or row.get("publishDate") or row.get("createTime") or row.get("gmtCreate") or row.get("modifyTime")
                employment_type = row.get("employmentType") or row.get("jobType") or row.get("recruitType")
                item = normalize(job_id, title, url, clean(location), clean(department), clean(employment_type),
                                 description, posted_at, COMPANY_NAME, raw_payload=row, apply_url=url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Alibaba] Page {page}: {len(rows)} source rows, {added} normalized, {len(output)} cumulative / {total}")
            if (total is not None and page * PAGE_SIZE >= int(total)) or len(rows) < PAGE_SIZE:
                break
    print(f"[Alibaba] Complete: {len(output)} jobs")
    return output
