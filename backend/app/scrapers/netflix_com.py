"""Netflix Careers scraper for the current Explore Jobs portal."""
from __future__ import annotations
import html as html_lib
import json
import os
import re
from datetime import datetime, timezone
import requests
from .auto import scrape as _auto_scrape
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Netflix"
CAREERS_URL = "https://explore.jobs.netflix.net/careers?domain=netflix.com"
OFFICIAL_DOMAIN = "netflix.com"
CSV_RANK = 6
MAX_PAGES = max(1, min(100, int(os.getenv("NETFLIX_MAX_PAGES", "30"))))
MAX_JOBS = max(0, int(os.getenv("NETFLIX_MAX_JOBS", "0")))
FETCH_DETAILS = os.getenv("NETFLIX_FETCH_DETAILS", "0").strip().lower() in {"1", "true", "yes"}
DETAIL_LIMIT = max(0, int(os.getenv("NETFLIX_DETAIL_LIMIT", "20")))

def _array_at(text, start):
    depth, quoted, escaped = 0, False, False
    for i in range(start, len(text)):
        c = text[i]
        if quoted:
            if escaped: escaped = False
            elif c == "\\": escaped = True
            elif c == '"': quoted = False
        elif c == '"': quoted = True
        elif c == "[": depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0: return text[start:i + 1]
    return None

def _positions(page_html):
    text = html_lib.unescape(page_html)
    found = []
    for m in re.finditer(r'"positions"\s*:\s*\[', text):
        raw = _array_at(text, m.end() - 1)
        try: rows = json.loads(raw) if raw else []
        except (ValueError, TypeError): continue
        if isinstance(rows, list):
            jobs = [x for x in rows if isinstance(x, dict) and (x.get("canonicalPositionUrl") or x.get("posting_name") or x.get("ats_job_id"))]
            if jobs: found.append(jobs)
    total_match = re.search(r'"count"\s*:\s*(\d+)', text)
    return (max(found, key=len) if found else []), (int(total_match.group(1)) if total_match else None)

def _detail(session, url):
    try:
        response = session.get(url, timeout=TIMEOUT)
        if response.status_code != 200: return None, None
        text = html_lib.unescape(response.text)
        for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', text, re.I | re.S):
            try: data = json.loads(m.group(1).strip())
            except (ValueError, TypeError): continue
            for item in data if isinstance(data, list) else [data]:
                if isinstance(item, dict) and item.get("@type") == "JobPosting":
                    return clean(item.get("description")), item.get("datePosted")
    except requests.RequestException: pass
    return None, None

def scrape(token: str | None = None):
    if token and token.strip(): return _auto_scrape(token.strip())
    session = requests.Session()
    session.headers.update(HEADERS)
    out, seen, total, detail_count = [], set(), None, 0
    for page in range(1, MAX_PAGES + 1):
        response = session.get(CAREERS_URL, params={"page": page}, timeout=TIMEOUT)
        response.raise_for_status()
        rows, page_total = _positions(response.text)
        total = page_total or total
        print(f"[Netflix] Page {page}: {len(rows)} embedded positions; total={total}")
        if not rows: break
        added = 0
        for row in rows:
            job_id = clean(row.get("id") or row.get("ats_job_id") or row.get("display_job_id"))
            title = clean(row.get("posting_name") or row.get("name") or row.get("title"))
            if not job_id or not title or job_id in seen: continue
            seen.add(job_id); added += 1
            url = clean(row.get("canonicalPositionUrl") or row.get("url")) or f"https://explore.jobs.netflix.net/careers/job/{job_id}"
            locs = row.get("locations") or row.get("location")
            location = ", ".join(clean(x) for x in locs if x) if isinstance(locs, list) else clean(locs)
            description = clean(row.get("job_description") or row.get("description"))
            posted = row.get("datePosted") or row.get("posted_at")
            if not posted and row.get("t_create"):
                try: posted = datetime.fromtimestamp(int(row["t_create"]), timezone.utc).isoformat()
                except (TypeError, ValueError, OSError): posted = None
            if FETCH_DETAILS and detail_count < DETAIL_LIMIT:
                detail_desc, detail_posted = _detail(session, url)
                description, posted = detail_desc or description, detail_posted or posted
                detail_count += 1
            item = normalize(job_id, title, url, location, clean(row.get("department") or row.get("business_unit")),
                             row.get("work_type") or row.get("employment_type"), description, posted,
                             COMPANY_NAME, raw_payload=row, apply_url=url)
            if item: out.append(item)
            if MAX_JOBS and len(out) >= MAX_JOBS: break
        if (MAX_JOBS and len(out) >= MAX_JOBS) or not added: break
        if total is not None and len(seen) >= total: break
        if len(rows) < 10: break
    if out:
        print(f"[Netflix] Complete: {len(out)} jobs; source total={total}; details fetched={detail_count}")
        return out
    print("[Netflix] No embedded jobs found; falling back to official page parser")
    return _auto_scrape(CAREERS_URL)
