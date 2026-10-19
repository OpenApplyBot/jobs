"""Netflix Jobs scraper using the public search API linked by its careers site.

The API returns postings under records.postings. Results are paginated and
normalized to the shared job schema; no account or session is required.
"""
from __future__ import annotations

import os
from urllib.parse import urlencode

import requests

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Netflix"
CAREERS_URL = "https://jobs.netflix.com/"
SEARCH_URL = "https://jobs.netflix.com/api/search"
OFFICIAL_DOMAIN = "netflix.com"
CSV_RANK = 6
MAX_PAGES = max(1, min(100, int(os.getenv("NETFLIX_MAX_PAGES", "30"))))
PAGE_SIZE = max(1, min(100, int(os.getenv("NETFLIX_PAGE_SIZE", "50"))))


def _postings(payload):
    records = payload.get("records") or {}
    if isinstance(records, dict):
        postings = records.get("postings") or []
        total = records.get("total") or records.get("total_count") or records.get("totalCount")
    else:
        postings, total = [], None
    if not isinstance(postings, list):
        postings = []
    return postings, total


def scrape(token: str | None = None):
    """Fetch Netflix's public postings API with bounded page traversal."""
    out = []
    seen = set()
    session = requests.Session()
    headers = {
        **HEADERS,
        "Accept": "application/json, text/plain, */*",
        "Referer": CAREERS_URL,
    }
    base_url = token.strip() if token and token.strip() else SEARCH_URL

    for page in range(1, MAX_PAGES + 1):
        response = session.get(
            base_url,
            params={"page": page, "size": PAGE_SIZE},
            headers=headers,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        rows, total = _postings(payload)
        if not rows:
            break

        for row in rows:
            if not isinstance(row, dict):
                continue
            job_id = row.get("external_id") or row.get("id") or row.get("lever_id")
            slug = clean(row.get("slug"))
            if not job_id and not slug:
                continue
            identity = str(job_id or slug)
            if identity in seen:
                continue
            seen.add(identity)

            job_url = clean(row.get("url") or row.get("job_url"))
            if not job_url:
                path_id = slug or job_id
                job_url = f"https://jobs.netflix.com/jobs/{path_id}"
            title = clean(row.get("text") or row.get("title") or row.get("name"))
            location = clean(row.get("location") or row.get("locations"))
            team = row.get("team") or row.get("subteam") or row.get("organization")
            description = row.get("description") or row.get("description_text")
            item = normalize(
                identity,
                title,
                job_url,
                location,
                clean(team),
                row.get("employment_type") or row.get("employmentType"),
                description,
                row.get("updated_at") or row.get("created_at"),
                COMPANY_NAME,
                raw_payload=row,
                apply_url=job_url,
            )
            if item:
                out.append(item)

        print(f"[Netflix] Page {page}: {len(rows)} source rows, {len(out)} unique jobs")
        if len(rows) < PAGE_SIZE:
            break
        try:
            total_count = int(total)
            if len(out) >= total_count:
                break
        except (TypeError, ValueError):
            pass

    print(f"[Netflix] Complete: {len(out)} jobs")
    return out
