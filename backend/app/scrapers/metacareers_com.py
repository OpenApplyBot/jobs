"""Meta Careers scraper using the public Relay GraphQL job-search endpoint."""
from __future__ import annotations

import json
import os
import re
import requests

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Meta"
CAREERS_URL = "https://www.metacareers.com/jobs"
BOOTSTRAP_URL = CAREERS_URL
GRAPHQL_URL = "https://www.metacareers.com/api/graphql/"
DETAIL_URL = "https://www.metacareers.com/jobs/{job_id}/"
LIST_DOC_ID = "29615178951461218"
OFFICIAL_DOMAIN = "metacareers.com"
CSV_RANK = 5
MAX_JOBS = max(0, int(os.getenv("META_MAX_JOBS", "0")))
FETCH_DETAILS = os.getenv("META_FETCH_DETAILS", "0").strip().lower() in {"1", "true", "yes"}
DETAIL_LIMIT = max(0, int(os.getenv("META_DETAIL_LIMIT", "20")))
LSD_RE = re.compile(r'"LSD",\[\],\{"token":"([^"]+)"')

def _new_session(bootstrap_url=BOOTSTRAP_URL):
    session = requests.Session()
    session.headers.update({
        **HEADERS,
        "Accept-Language": "en-US,en;q=0.9",
        "Upgrade-Insecure-Requests": "1",
    })
    response = session.get(bootstrap_url, timeout=TIMEOUT)
    response.raise_for_status()
    match = LSD_RE.search(response.text)
    if not match:
        raise RuntimeError("Meta careers bootstrap page did not expose the public LSD token")
    return session, match.group(1)

def _fetch_all_jobs(session, lsd, bootstrap_url=BOOTSTRAP_URL):
    form = {
        "lsd": lsd,
        "doc_id": LIST_DOC_ID,
        "variables": json.dumps({"search_input": {}}, separators=(",", ":")),
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.metacareers.com",
        "Referer": bootstrap_url,
        "X-FB-LSD": lsd,
        "X-FB-Friendly-Name": "CareersJobSearchResultsDataQuery",
    }
    response = session.post(GRAPHQL_URL, data=form, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    node = (payload.get("data") or {}).get("job_search_with_featured_jobs")
    if not isinstance(node, dict):
        raise RuntimeError(f"Meta GraphQL response did not contain job_search_with_featured_jobs: {list(payload)[:10]}")
    jobs = node.get("all_jobs") or []
    if not isinstance(jobs, list):
        raise RuntimeError("Meta GraphQL all_jobs field was not a list")
    return jobs

def _extract_detail(session, job_id):
    try:
        response = session.get(DETAIL_URL.format(job_id=job_id), timeout=TIMEOUT)
        if response.status_code != 200:
            return None, None
        for match in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', response.text, re.I | re.S):
            try:
                data = json.loads(match.group(1).strip())
            except (ValueError, TypeError):
                continue
            candidates = data if isinstance(data, list) else [data]
            for item in candidates:
                if isinstance(item, dict) and item.get("@type") == "JobPosting":
                    return clean(item.get("description")), item.get("datePosted")
    except requests.RequestException:
        pass
    return None, None

def scrape(token: str | None = None):
    """Fetch public Meta jobs, with optional bounded detail-page enrichment."""
    page = token.strip() if token and token.strip() else BOOTSTRAP_URL
    session, lsd = _new_session(page)
    source_jobs = _fetch_all_jobs(session, lsd, page)
    out, seen = [], set()
    details_done = 0
    for row in source_jobs:
        if not isinstance(row, dict):
            continue
        job_id = clean(row.get("id") or row.get("job_id"))
        title = clean(row.get("title"))
        if not job_id or not title or job_id in seen:
            continue
        seen.add(job_id)
        locations = row.get("locations") or []
        if isinstance(locations, str):
            locations = [locations]
        location = ", ".join(clean(item) for item in locations if item)
        teams = row.get("teams") or []
        sub_teams = row.get("sub_teams") or []
        if isinstance(teams, str):
            teams = [teams]
        if isinstance(sub_teams, str):
            sub_teams = [sub_teams]
        department = ", ".join(clean(item) for item in [*teams, *sub_teams] if item)
        job_url = DETAIL_URL.format(job_id=job_id)
        description = None
        posted_at = row.get("date_posted") or row.get("datePosted")
        if FETCH_DETAILS and details_done < DETAIL_LIMIT:
            description, detail_posted = _extract_detail(session, job_id)
            posted_at = detail_posted or posted_at
            details_done += 1
        item = normalize(
            job_id, title, job_url, location, department,
            row.get("employment_type") or row.get("employmentType"),
            description, posted_at, COMPANY_NAME,
            raw_payload=row, apply_url=job_url,
        )
        if item:
            out.append(item)
        if MAX_JOBS and len(out) >= MAX_JOBS:
            break
    print(f"[Meta] Source jobs={len(source_jobs)}; normalized jobs={len(out)}; detail pages fetched={details_done}")
    return out
