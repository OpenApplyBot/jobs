"""Dell Technologies scraper: public jobs API with first-party SSR fallback."""
from __future__ import annotations
import json
import os
import re
import requests
from urllib.parse import urljoin
from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "Dell Technologies"
CAREERS_URL = "https://jobs.dell.com/en/search-jobs"
API_URL = "https://jobs.dell.com/api/jobs"
OFFICIAL_DOMAIN = "jobs.dell.com"
CSV_RANK = 30
PAGE_SIZE = max(1, min(100, int(os.getenv("DELL_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("DELL_MAX_PAGES", "2"))))

def _balanced(text, start, opening="[", closing="]"):
    if start < 0:
        return None
    quote = None
    escaped = False
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
        elif ch == opening:
            depth += 1
        elif ch == closing:
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None

def _ssr_rows(html):
    marker = html.find("eagerLoadRefineSearch")
    if marker >= 0:
        match = re.search(r"""["']jobs["']\s*:\s*\[""", html[marker:])
        if match:
            start = marker + match.end() - 1
            raw = _balanced(html, start)
            if raw:
                try:
                    value = json.loads(raw)
                    if isinstance(value, list):
                        return [x for x in value if isinstance(x, dict)]
                except (ValueError, TypeError):
                    pass
    rows = []
    for match in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.I | re.S):
        try:
            value = json.loads(match.group(1).strip())
        except (ValueError, TypeError):
            continue
        for item in value if isinstance(value, list) else [value]:
            if isinstance(item, dict) and item.get("@type") == "JobPosting":
                rows.append(item)
    return rows

def _normalize_rows(rows, source="api"):
    output, seen = [], set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        row = row.get("data") if isinstance(row.get("data"), dict) else row
        identifier = row.get("jobSeqNo") or row.get("id") or row.get("jobId") or row.get("req_id") or row.get("identifier")
        if isinstance(identifier, dict):
            identifier = identifier.get("value")
        job_id = clean(identifier)
        title = clean(row.get("title") or row.get("name") or row.get("jobTitle") or row.get("name"))
        if not job_id or not title or job_id in seen:
            continue
        seen.add(job_id)
        raw_url = clean(row.get("url") or row.get("canonical_url") or row.get("applyUrl") or row.get("jobUrl"))
        url = urljoin("https://jobs.dell.com", raw_url) if raw_url else f"https://jobs.dell.com/en/job/{job_id}"
        location = row.get("location") or row.get("locations") or row.get("full_location") or row.get("jobLocation")
        if isinstance(location, (dict, list)):
            location = location_text(location)
        description = clean(row.get("description") or row.get("content") or row.get("jobDescription"))
        item = normalize(job_id, title, url, clean(location), clean(row.get("category") or row.get("department")),
                         clean(row.get("employmentType") or row.get("jobType")), description,
                         row.get("postedDate") or row.get("posted_date") or row.get("datePosted"),
                         COMPANY_NAME, raw_payload={"source": source, **row}, apply_url=clean(row.get("applyUrl")) or url)
        if item:
            output.append(item)
    return output

def scrape(token: str | None = None):
    page_url = token.strip() if token and token.strip() else CAREERS_URL
    headers = {**HEADERS, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
               "Accept": "application/json, text/plain, */*", "Referer": page_url, "Origin": "https://jobs.dell.com"}
    output, seen = [], set()
    with requests.Session() as session:
        session.headers.update(headers)
        page = session.get(page_url, timeout=TIMEOUT)
        page.raise_for_status()
        for page_no in range(1, MAX_PAGES + 1):
            try:
                response = session.get(API_URL, params={"page": page_no, "limit": PAGE_SIZE, "sortBy": "relevance",
                                                         "descending": "false", "internal": "false"}, timeout=TIMEOUT)
                if response.status_code in (401, 403, 404, 429):
                    print(f"[Dell] Jobs API unavailable (HTTP {response.status_code}); falling back to official page data")
                    break
                response.raise_for_status()
                payload = response.json()
            except (requests.RequestException, ValueError) as exc:
                print(f"[Dell] Jobs API failed ({exc}); falling back to official page data")
                break
            node = payload.get("data") if isinstance(payload.get("data"), dict) else payload
            rows = node.get("jobs") or node.get("list") or node.get("items") or []
            total = node.get("total") or node.get("totalCount") or node.get("count")
            if not rows:
                break
            normalized = _normalize_rows(rows, "Dell public jobs API")
            for item in normalized:
                if item.get("source_job_id") not in seen:
                    seen.add(item.get("source_job_id"))
                    output.append(item)
            print(f"[Dell] API page {page_no}: {len(rows)} source rows, {len(output)} normalized total")
            if (total and page_no * PAGE_SIZE >= int(total)) or len(rows) < PAGE_SIZE:
                break
        if not output:
            ssr = _ssr_rows(page.text)
            output = _normalize_rows(ssr, "Dell official careers SSR")
            print(f"[Dell] Official page SSR fallback: {len(output)} listings")
    if not output:
        raise RuntimeError("Dell official careers page/API returned no normalized listings")
    print(f"[Dell] Complete: {len(output)} jobs")
    return output
