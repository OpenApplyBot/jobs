"""Adobe Careers scraper using the public Phenom server-rendered job data."""
from __future__ import annotations

import json
import os
import re
import requests
from urllib.parse import urljoin

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Adobe"
CAREERS_URL = "https://careers.adobe.com/us/en/search-results"
OFFICIAL_DOMAIN = "careers.adobe.com"
CSV_RANK = 24
MAX_PAGES = max(1, min(20, int(os.getenv("ADOBE_MAX_PAGES", "1"))))

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

def _find_jobs(html):
    # Phenom embeds the first result page under eagerLoadRefineSearch.data.jobs.
    marker = html.find("eagerLoadRefineSearch")
    if marker >= 0:
        jobs_key = re.search(r"""["']jobs["']\s*:\s*\[""", html[marker:])
        if jobs_key:
            array_start = marker + jobs_key.end() - 1
            raw = _balanced(html, array_start, "[", "]")
            if raw:
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        return [x for x in parsed if isinstance(x, dict)]
                except (ValueError, TypeError):
                    pass
    # Fall back to a JSON-LD JobPosting array when the Phenom blob changes.
    jobs = []
    for match in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.I | re.S):
        try:
            value = json.loads(match.group(1).strip())
        except (ValueError, TypeError):
            continue
        values = value if isinstance(value, list) else [value]
        for item in values:
            if isinstance(item, dict) and item.get("@type") == "JobPosting":
                jobs.append(item)
    return jobs

def scrape(token: str | None = None):
    base_url = token.strip() if token and token.strip() else CAREERS_URL
    output, seen = [], set()
    with requests.Session() as session:
        session.headers.update({**HEADERS, "Accept": "text/html,application/xhtml+xml", "Referer": "https://careers.adobe.com/us/en/"})
        for page in range(1, MAX_PAGES + 1):
            response = session.get(base_url, params={"page": page}, timeout=TIMEOUT)
            response.raise_for_status()
            rows = _find_jobs(response.text)
            if not rows:
                if page == 1:
                    raise RuntimeError("Adobe Phenom careers page did not expose job records in SSR data or JSON-LD")
                break
            added = 0
            for row in rows:
                job_id = clean(row.get("jobSeqNo") or row.get("jobId") or row.get("id") or row.get("identifier"))
                title = clean(row.get("title") or row.get("jobTitle") or row.get("name"))
                if isinstance(row.get("identifier"), dict):
                    job_id = job_id or clean(row["identifier"].get("value"))
                if not job_id or not title or job_id in seen:
                    continue
                seen.add(job_id)
                raw_url = clean(row.get("url") or row.get("applyUrl") or row.get("jobUrl"))
                job_url = urljoin("https://careers.adobe.com", raw_url) if raw_url else f"https://careers.adobe.com/us/en/job/{job_id}"
                location = row.get("location") or row.get("jobLocation") or row.get("locations")
                if isinstance(location, dict):
                    location = location.get("name") or location.get("address", {}).get("addressLocality")
                elif isinstance(location, list):
                    location = ", ".join(clean(x.get("name") if isinstance(x, dict) else x) for x in location if x)
                description = clean(row.get("description") or row.get("jobDescription") or row.get("summary"))
                item = normalize(job_id, title, job_url, clean(location), clean(row.get("category") or row.get("team")),
                                 clean(row.get("employmentType") or row.get("jobType")), description,
                                 row.get("postedDate") or row.get("datePosted"), COMPANY_NAME,
                                 raw_payload=row, apply_url=clean(row.get("applyUrl")) or job_url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Adobe] Page {page}: {len(rows)} SSR jobs, {added} new, {len(output)} total")
            if added == 0 or len(rows) < 10:
                break
    if not output:
        raise RuntimeError("Adobe official careers page returned no normalized job records")
    print(f"[Adobe] Complete: {len(output)} jobs")
    return output
