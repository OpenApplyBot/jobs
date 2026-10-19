"""Apple Jobs scraper using the public JSON search endpoint on jobs.apple.com."""
from __future__ import annotations

from html import unescape
from urllib.parse import urlparse
import json
import os
import re

import requests

from .common import clean, get, normalize, location_text

COMPANY_NAME = "Apple"
CAREERS_URL = "https://jobs.apple.com/en-us/search"
SEARCH_URL = "https://jobs.apple.com/api/v1/search"
OFFICIAL_DOMAIN = "apple.com"
CSV_RANK = 4

MAX_PAGES = max(1, int(os.getenv("APPLE_MAX_PAGES", "30")))
# Apple's API returns 20 rows per page regardless of a requested page-size setting.
PAGE_SIZE = 20
FETCH_DETAILS = os.getenv("APPLE_FETCH_DETAILS", "0").lower() not in {"0", "false", "no"}
LOCALE = os.getenv("APPLE_LOCALE", "en-us").strip().lower() or "en-us"
TIMEOUT = max(5, int(os.getenv("APPLE_HTTP_TIMEOUT", "20")))


class ScrapeBatch(list):
    """List-compatible Apple scrape result with full-scan readiness metadata."""

    def __init__(self, rows=(), *, incremental_ready=False):
        super().__init__(rows)
        self.incremental_ready = incremental_ready


HEADERS = {
    "User-Agent": "OpenApplyBot-Jobs/1.0 (+https://github.com/OpenApplyBot/jobs; public job indexer)",
    "Accept": "application/json, text/html;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://jobs.apple.com",
    "Referer": CAREERS_URL,
}
DETAIL_HEADERS = {
    "User-Agent": HEADERS["User-Agent"],
    "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _post(url: str, payload: dict):
    response = requests.post(url, json=payload, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    final = urlparse(response.url)
    if final.scheme != "https" or final.hostname != "jobs.apple.com":
        raise ValueError(f"Unexpected redirect for Apple Careers request: {response.url}")
    return response.json()


def _unwrap(payload):
    if not isinstance(payload, dict):
        return {}
    value = payload.get("res")
    if isinstance(value, dict):
        return value
    value = payload.get("data")
    if isinstance(value, dict):
        return value
    return payload


def _first(item, *keys):
    for key in keys:
        value = item.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def _text(value):
    if isinstance(value, str):
        return clean(value)
    if isinstance(value, dict):
        return clean(_first(value, "text", "name", "label", "value", "description", "html"))
    if isinstance(value, list):
        return ", ".join(part for part in (_text(v) for v in value) if part) or None
    return clean(value)


def _rows(payload):
    data = _unwrap(payload)
    for key in ("searchResults", "results", "jobs", "postings", "positions", "items"):
        rows = data.get(key)
        if isinstance(rows, list):
            return rows, _first(data, "totalRecords", "total_records", "total", "count")
    for value in data.values():
        if isinstance(value, dict):
            for key in ("searchResults", "results", "jobs", "postings", "positions", "items"):
                rows = value.get(key)
                if isinstance(rows, list):
                    return rows, _first(value, "totalRecords", "total_records", "total", "count")
    return [], _first(data, "totalRecords", "total_records", "total", "count")


def _slug(title):
    title = clean(title) or "role"
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", title.lower())).strip("-")[:180] or "role"


def _job_url(item, job_id, title):
    value = _first(item, "url", "jobUrl", "job_url", "canonicalUrl", "canonical_url")
    if value:
        if str(value).startswith("/"):
            value = "https://jobs.apple.com" + str(value)
        parsed = urlparse(str(value))
        if parsed.scheme == "https" and parsed.hostname == "jobs.apple.com":
            return str(value)
    slug = _first(item, "transformedPostingTitle", "transformed_posting_title", "slug") or _slug(title)
    # Apple URLs use /details/{numeric position id}/{slug}, not /details/{slug}/{id}.
    return f"https://jobs.apple.com/{LOCALE}/details/{job_id}/{slug}"


def _normalize(item):
    if not isinstance(item, dict):
        return None
    job_id = _first(item, "positionId", "position_id", "jobId", "job_id", "id", "postingId")
    title = _text(_first(item, "postingTitle", "posting_title", "title", "jobTitle", "job_title", "name"))
    if not job_id or not title:
        return None
    job_id = str(job_id)
    url = _job_url(item, job_id, title)
    location_value = _first(item, "locations", "location", "locationName", "location_name")
    location = _text(location_value) or location_text(location_value)
    team = _first(item, "team", "teamName", "team_name", "department", "jobFunction")
    department = _text(team)
    if isinstance(team, dict):
        department = _text(_first(team, "teamName", "name", "label"))
    employment_type = _text(_first(item, "employmentType", "employment_type", "scheduleType"))
    description = _text(_first(item, "jobSummary", "job_summary", "summary", "description", "descriptionHtml", "jobDescription"))
    posted = _first(item, "postingDate", "posting_date", "datePosted", "date_posted", "postedAt")
    return normalize(
        job_id, title, url,
        location=location,
        department=department,
        employment_type=employment_type,
        description=description,
        posted_at=_text(posted),
        company=COMPANY_NAME,
        raw_payload=item,
        apply_url=url,
    )


def _hydration(html):
    """Decode Apple's server-rendered JSON.parse string used by job detail pages."""
    marker = "window.__staticRouterHydrationData"
    start = html.find(marker)
    if start < 0:
        return None
    segment = html[start:]
    needle = 'JSON.parse("'
    start_literal = segment.find(needle)
    if start_literal < 0:
        return None
    cursor = start_literal + len(needle)
    end = cursor
    while True:
        end = segment.find('")', end)
        if end < 0:
            return None
        if segment[end - 1] != "\\":
            break
        end += 1
    raw = segment[cursor:end]
    try:
        return json.loads(json.loads(f'"{raw}"'))
    except (json.JSONDecodeError, ValueError):
        return None


def _fetch_detail(item):
    job_id = str(_first(item, "positionId", "position_id", "jobId", "job_id", "id", "postingId") or "")
    title = _text(_first(item, "postingTitle", "posting_title", "title", "jobTitle", "job_title", "name")) or "job"
    slug = _first(item, "transformedPostingTitle", "transformed_posting_title", "slug") or _slug(title)
    if not job_id:
        return item
    detail_url = f"https://jobs.apple.com/{LOCALE}/details/{job_id}/{slug}"
    try:
        response = get(detail_url)
        final = urlparse(response.url)
        if final.scheme != "https" or final.hostname != "jobs.apple.com":
            raise ValueError(f"Unexpected redirect for Apple detail request: {response.url}")
        data = _hydration(response.text)
        if not isinstance(data, dict):
            print(f"[Apple] Detail page had no parseable hydration data for {job_id}", flush=True)
            return item
        details = (data.get("loaderData") or {}).get("jobDetails")
        if not isinstance(details, dict):
            return item
        jobs_data = details.get("jobsData")
        if isinstance(jobs_data, list):
            detail = jobs_data[0] if jobs_data and isinstance(jobs_data[0], dict) else {}
        elif isinstance(jobs_data, dict):
            detail = jobs_data
        else:
            detail = {}
        merged = dict(item)
        merged.update({k: v for k, v in detail.items() if v not in (None, "", [], {})})
        return merged
    except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
        print(f"[Apple] Detail lookup unavailable for {job_id}: {exc}", flush=True)
        return item


def _search_page(page):
    payload = {
        "query": "",
        "filters": {},
        "page": page,
        "locale": LOCALE,
        "sort": "newest",
        "format": {
            "longDate": "MMMM D, YYYY",
            "mediumDate": "MMM D, YYYY",
        },
    }
    response = _post(SEARCH_URL, payload)
    rows, total = _rows(response)
    return rows, total


def scrape(token: str | None = None, known_job_ids=None):
    """Fetch Apple careers jobs, stopping at an existing-only page on newest-first feeds.

    Apple explicitly requests newest-first results. After a prior successful run,
    a page containing only known source IDs is a safe incremental checkpoint:
    new listings should have appeared before it. The already-seen rows from the
    scanned pages are still returned so the worker can verify/touch them.
    """
    token = (token or "").strip()
    if token:
        parsed = urlparse(token)
        if parsed.scheme not in {"http", "https"} or parsed.hostname != "jobs.apple.com":
            raise ValueError(f"Refusing non-Apple Careers URL: {token}")
        # Actual Apple format is /{locale}/details/{numeric-id}/{slug}.
        match = re.search(r"/details/(\d+)(?:/([^/?#]+))?", parsed.path)
        if not match:
            raise ValueError("Apple token URL must be an official /details/<job-id>/<slug> URL")
        job_id, slug = match.group(1), match.group(2) or "job"
        item = {"positionId": job_id, "postingTitle": slug.replace("-", " "), "transformedPostingTitle": slug, "url": token}
        return [row] if (row := _normalize(_fetch_detail(item) if FETCH_DETAILS else item)) else []

    print(f"[Apple] Starting official careers search; API page size={PAGE_SIZE}, max pages={MAX_PAGES}", flush=True)
    discovered = {}
    incremental_mode = known_job_ids is not None and bool(known_job_ids)
    known_ids = {str(job_id) for job_id in (known_job_ids or set())}
    total_reported = None
    source_complete = False
    checkpoint_reached = False
    for page in range(1, MAX_PAGES + 1):
        try:
            rows, total = _search_page(page)
        except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Apple Careers search failed on page {page}: {exc}") from exc
        if total is not None:
            try:
                total_reported = int(total)
            except (TypeError, ValueError):
                pass
        new_count = 0
        known_on_page = 0
        new_on_page = 0
        for item in rows:
            row = _normalize(item)
            if row and row["url"] not in discovered:
                discovered[row["url"]] = item
                new_count += 1
                if known_ids and row["source_job_id"] in known_ids:
                    known_on_page += 1
                else:
                    new_on_page += 1
        print(
            f"[Apple] Page {page}: {len(rows)} source rows, {len(discovered)} normalized unique jobs"
            + (f" / {total_reported} reported" if total_reported is not None else ""),
            flush=True,
        )
        if not rows:
            source_complete = total_reported is None or len(discovered) >= total_reported
            break
        if new_count == 0:
            # A repeated page is not proof that pagination reached the end when
            # an advertised total says more records should exist.
            source_complete = total_reported is not None and len(discovered) >= total_reported
            break
        if incremental_mode and known_on_page > 0 and new_on_page == 0:
            checkpoint_reached = True
            print(f"[Apple] Incremental checkpoint reached on page {page}; stopping after {len(discovered)} verified listings", flush=True)
            break
        if total_reported is not None and page * PAGE_SIZE >= total_reported:
            source_complete = True
            break
        if total_reported is None and len(rows) < PAGE_SIZE:
            source_complete = True
            break

    items = list(discovered.values())
    if FETCH_DETAILS and items:
        print(f"[Apple] Enriching {len(items)} records with detail pages", flush=True)
        enriched = []
        for index, item in enumerate(items, 1):
            row = _normalize(_fetch_detail(item))
            if row:
                enriched.append(row)
            if index % 20 == 0 or index == len(items):
                print(f"[Apple] Details processed: {index}/{len(items)}", flush=True)
        result = list({row["url"]: row for row in enriched}.values())
    else:
        result = [row for item in items if (row := _normalize(item))]
    incremental_ready = checkpoint_reached or source_complete
    if not incremental_ready:
        print("[Apple] Full scan did not reach a confirmed end; incremental early-stop remains disabled", flush=True)
    print(f"[Apple] Complete: {len(result)} jobs; reported total={total_reported if total_reported is not None else 'unknown'}", flush=True)
    return ScrapeBatch(result, incremental_ready=incremental_ready)
