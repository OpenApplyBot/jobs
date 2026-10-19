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
DETAIL_URL = "https://jobs.apple.com/api/v1/details"
OFFICIAL_DOMAIN = "apple.com"
CSV_RANK = 4

MAX_PAGES = max(1, int(os.getenv("APPLE_MAX_PAGES", "30")))
PAGE_SIZE = max(1, min(20, int(os.getenv("APPLE_PAGE_SIZE", "20"))))
FETCH_DETAILS = os.getenv("APPLE_FETCH_DETAILS", "0").lower() not in {"0", "false", "no"}
LOCALE = os.getenv("APPLE_LOCALE", "en-us").strip().lower() or "en-us"
TIMEOUT = max(5, int(os.getenv("APPLE_HTTP_TIMEOUT", "20")))
HEADERS = {
    "User-Agent": "OpenApplyBot-Jobs/1.0 (+https://github.com/OpenApplyBot/jobs; public job indexer)",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://jobs.apple.com",
    "Referer": CAREERS_URL,
}


def _post(url: str, payload: dict):
    response = requests.post(url, json=payload, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    final = urlparse(response.url)
    if final.scheme != "https" or final.hostname != "jobs.apple.com":
        raise ValueError(f"Unexpected redirect for Apple Careers request: {response.url}")
    return response.json()


def _unwrap(payload):
    """Return the nested response object while tolerating API envelope changes."""
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
    # Some responses wrap the search result array one level deeper.
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
    slug = _first(item, "transformedPostingTitle", "transformed_posting_title", "slug")
    return f"https://jobs.apple.com/{LOCALE}/details/{slug or _slug(title)}/{job_id}"


def _normalize(item):
    if not isinstance(item, dict):
        return None
    job_id = _first(item, "positionId", "position_id", "jobId", "job_id", "id", "postingId")
    title = _text(_first(item, "postingTitle", "posting_title", "title", "jobTitle", "job_title", "name"))
    if not job_id or not title:
        return None
    url = _job_url(item, str(job_id), title)
    location = _text(_first(item, "locations", "location", "locationName", "location_name"))
    if not location:
        location = location_text(_first(item, "locations", "location"))
    department = _text(_first(item, "team", "teamName", "team_name", "department", "jobFunction"))
    employment_type = _text(_first(item, "employmentType", "employment_type", "scheduleType"))
    description = _text(_first(item, "jobSummary", "job_summary", "summary", "description", "descriptionHtml"))
    posted = _first(item, "postingDate", "posting_date", "datePosted", "date_posted", "postedAt")
    return normalize(
        str(job_id), title, url,
        location=location,
        department=department,
        employment_type=employment_type,
        description=description,
        posted_at=_text(posted),
        company=COMPANY_NAME,
        raw_payload=item,
        apply_url=url,
    )


def _fetch_detail(item):
    job_id = _first(item, "positionId", "position_id", "jobId", "job_id", "id", "postingId")
    if not job_id:
        return item
    # This is the same public detail route used by the Apple Careers frontend.
    try:
        payload = _post(f"{DETAIL_URL}/{job_id}/{LOCALE}", {})
        detail = _unwrap(payload)
        for key in ("job", "posting", "details", "jobDetails"):
            if isinstance(detail.get(key), dict):
                detail = detail[key]
                break
        if isinstance(detail, dict):
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
        "sort": "",
        "format": {
            "longDate": "MMMM D, YYYY",
            "mediumDate": "MMM D, YYYY",
        },
    }
    response = _post(SEARCH_URL, payload)
    rows, total = _rows(response)
    return rows, total


def scrape(token: str | None = None):
    """Fetch Apple careers jobs; optional token may be an Apple job-detail URL."""
    token = (token or "").strip()
    if token:
        parsed = urlparse(token)
        if parsed.scheme not in {"http", "https"} or parsed.hostname != "jobs.apple.com":
            raise ValueError(f"Refusing non-Apple Careers URL: {token}")
        match = re.search(r"/details/([^/?#]+)/(\d+)", parsed.path)
        if not match:
            raise ValueError("Apple token URL must be an official /details/<slug>/<job-id> URL")
        job_id = match.group(2)
        item = {"positionId": job_id, "postingTitle": match.group(1), "url": token}
        return [row] if (row := _normalize(_fetch_detail(item) if FETCH_DETAILS else item)) else []

    print(f"[Apple] Starting official careers search; page size={PAGE_SIZE}, max pages={MAX_PAGES}", flush=True)
    discovered = {}
    total_reported = None
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
        for item in rows:
            row = _normalize(item)
            if row and row["url"] not in discovered:
                discovered[row["url"]] = item
                new_count += 1
        print(
            f"[Apple] Page {page}: {len(rows)} source rows, {len(discovered)} normalized unique jobs"
            + (f" / {total_reported} reported" if total_reported is not None else ""),
            flush=True,
        )
        if not rows or new_count == 0:
            break
        if total_reported is not None and page * PAGE_SIZE >= total_reported:
            break

    items = list(discovered.values())
    if FETCH_DETAILS and items:
        print(f"[Apple] Enriching {len(items)} records with detail pages", flush=True)
        enriched = []
        for index, item in enumerate(items, 1):
            detail = _fetch_detail(item)
            row = _normalize(detail)
            if row:
                enriched.append(row)
            if index % 20 == 0 or index == len(items):
                print(f"[Apple] Details processed: {index}/{len(items)}", flush=True)
        output = {row["url"]: row for row in enriched}
        result = list(output.values())
    else:
        result = [row for item in items if (row := _normalize(item))]
    print(f"[Apple] Complete: {len(result)} jobs; reported total={total_reported if total_reported is not None else 'unknown'}", flush=True)
    return result
