"""Microsoft Careers scraper using the public Eightfold-powered careers endpoints.

The official careers frontend links to apply.careers.microsoft.com. The scraper
prefers the PCS-X search endpoint and falls back to the classic public jobs
endpoint when PCS-X is unavailable. It never requires an API key.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse
import json
import os
import re

import requests

from .common import get, normalize, location_text

COMPANY_NAME = "Microsoft"
CAREERS_URL = "https://careers.microsoft.com/v2/global/en/home.html"
SEARCH_URL = "https://apply.careers.microsoft.com/api/pcsx/search"
CLASSIC_URL = "https://apply.careers.microsoft.com/api/apply/v2/jobs"
DETAIL_URL = "https://apply.careers.microsoft.com/api/pcsx/position_details"
OFFICIAL_DOMAIN = "microsoft.com"
CSV_RANK = 2

MAX_PAGES = max(1, int(os.getenv("MICROSOFT_MAX_PAGES", "200")))
PAGE_SIZE = max(1, min(100, int(os.getenv("MICROSOFT_PAGE_SIZE", "10"))))
FETCH_DETAILS = os.getenv("MICROSOFT_FETCH_DETAILS", "1").lower() not in {"0", "false", "no"}
DETAIL_WORKERS = max(1, min(6, int(os.getenv("MICROSOFT_DETAIL_WORKERS", "4"))))
TIMEOUT = max(5, int(os.getenv("MICROSOFT_HTTP_TIMEOUT", "20")))
HEADERS = {
    "User-Agent": "OpenApplyBot-Jobs/1.0 (+https://github.com/OpenApplyBot/jobs; public job indexer)",
    "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _json_get(url, params):
    response = get(url, params=params)
    final_host = (urlparse(response.url).hostname or "").lower()
    if final_host not in {"apply.careers.microsoft.com", "careers.microsoft.com"}:
        raise ValueError(f"Unexpected redirect host for Microsoft careers request: {final_host}")
    return response.json()


def _items(payload):
    """Handle the known Eightfold JSON envelopes without assuming one exact shape."""
    if isinstance(payload, list):
        return payload, None
    if not isinstance(payload, dict):
        return [], None
    data = payload.get("data")
    if isinstance(data, dict):
        positions = data.get("positions") or data.get("jobs") or data.get("results")
        count = data.get("count") or data.get("total") or data.get("total_count")
        if isinstance(positions, list):
            return positions, count
    positions = payload.get("positions") or payload.get("jobs") or payload.get("results")
    count = payload.get("count") or payload.get("total") or payload.get("total_count")
    return (positions if isinstance(positions, list) else []), count


def _first(item, *keys):
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return value
    return None


def _as_text(value):
    if isinstance(value, str):
        return re.sub(r"\\s+", " ", value).strip() or None
    if isinstance(value, dict):
        return _first(value, "name", "label", "value", "city", "text")
    if isinstance(value, list):
        values = [_as_text(part) for part in value]
        return ", ".join(part for part in values if part) or None
    return str(value) if value is not None else None


def _timestamp(value):
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
        number = float(value)
        if number > 10_000_000_000:
            number /= 1000
        try:
            return datetime.fromtimestamp(number, tz=timezone.utc).isoformat()
        except (ValueError, OverflowError, OSError):
            return str(value)
    return str(value)


def _job_url(item):
    value = _first(
        item,
        "canonicalPositionUrl", "canonical_position_url",
        "positionUrl", "position_url", "url", "applyUrl", "apply_url",
    )
    job_id = _first(item, "id", "positionId", "position_id", "displayJobId", "display_job_id")
    if value:
        url = urljoin("https://apply.careers.microsoft.com/", str(value))
        parsed = urlparse(url)
        if parsed.scheme == "https" and parsed.hostname in {
            "apply.careers.microsoft.com", "careers.microsoft.com"
        }:
            return url
    if job_id:
        return f"https://apply.careers.microsoft.com/careers/job/{job_id}"
    return None


def _job_id(item, url):
    value = _first(item, "id", "positionId", "position_id", "displayJobId", "display_job_id", "atsJobId", "ats_job_id")
    if value is not None:
        return str(value)
    match = re.search(r"/(?:job|jobs)/([^/?#]+)", urlparse(url).path)
    return match.group(1) if match else url


def _location(item):
    value = _first(item, "locations", "standardizedLocations", "primaryLocation", "primary_location", "location", "locationName")
    if value is None:
        return None
    return location_text(value) or _as_text(value)


def _normalize(item):
    if not isinstance(item, dict):
        return None
    url = _job_url(item)
    title = _as_text(_first(item, "name", "posting_name", "title", "jobTitle", "job_title"))
    if not url or not title:
        return None
    description = _first(item, "job_description", "jobDescription", "description", "descriptionHtml", "description_html")
    if isinstance(description, dict):
        description = _first(description, "text", "html", "content")
    job_id = _job_id(item, url)
    department = _as_text(_first(item, "department", "businessUnit", "business_unit", "team", "category", "discipline"))
    employment_type = _as_text(_first(item, "employmentType", "employment_type", "roleType", "role_type"))
    posted = _timestamp(_first(item, "postedTs", "posted_ts", "creationTs", "creation_ts", "t_create", "datePosted", "posted_at"))
    return normalize(
        job_id, title, url,
        location=_location(item),
        department=department,
        employment_type=employment_type,
        description=description,
        posted_at=posted,
        company=_as_text(_first(item, "companyName", "company_name")) or COMPANY_NAME,
        raw_payload=item,
        apply_url=url,
    )


def _fetch_detail(item):
    job_id = _first(item, "id", "positionId", "position_id")
    if job_id is None:
        return item
    params = {"domain": "microsoft.com", "position_id": str(job_id), "hl": "en_us"}
    try:
        payload = _json_get(DETAIL_URL, params)
        if isinstance(payload, dict):
            data = payload.get("data")
            if isinstance(data, dict):
                payload = data
            if isinstance(payload, dict):
                # Some versions wrap the detail record in a position/job key.
                nested = payload.get("position") or payload.get("job")
                if isinstance(nested, dict):
                    payload = nested
                merged = dict(item)
                merged.update({key: value for key, value in payload.items() if value not in (None, "", [], {})})
                return merged
    except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
        print(f"[Microsoft] Detail lookup unavailable for {job_id}: {exc}", flush=True)
    return item


def _search_page(start):
    params = {
        "domain": "microsoft.com",
        "hl": "en_us",
        "start": start,
        "num": PAGE_SIZE,
    }
    errors = []
    for endpoint in (SEARCH_URL, CLASSIC_URL):
        try:
            payload = _json_get(endpoint, params)
            rows, count = _items(payload)
            if rows or (isinstance(payload, dict) and any(k in payload for k in ("positions", "data", "count", "total"))):
                return rows, count, endpoint
            errors.append(f"{endpoint}: response had no positions")
        except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{endpoint}: {exc}")
    raise RuntimeError("Microsoft Careers endpoints failed: " + " | ".join(errors))


def scrape(token: str | None = None):
    """Return normalized Microsoft job records.

    Optional environment settings:
      MICROSOFT_MAX_PAGES=200       safety cap on listing pages
      MICROSOFT_PAGE_SIZE=10        number requested per page (1-100)
      MICROSOFT_FETCH_DETAILS=0     listing-only mode for quick JSON tests
      MICROSOFT_DETAIL_WORKERS=4    concurrent detail requests (1-6)

    An explicit token can be a Microsoft careers job URL; otherwise the public
    listings endpoint is paginated using the API's start offset.
    """
    token = (token or "").strip()
    if token:
        parsed = urlparse(token)
        if parsed.scheme in {"http", "https"} and parsed.hostname in {
            "apply.careers.microsoft.com", "careers.microsoft.com"
        }:
            match = re.search(r"/(?:job|jobs)/([^/?#]+)", parsed.path)
            if match:
                job_id = match.group(1)
                try:
                    payload = _json_get(DETAIL_URL, {
                        "domain": "microsoft.com", "position_id": job_id, "hl": "en_us"
                    })
                    rows, _ = _items(payload)
                    detail = rows[0] if rows else payload.get("data", payload) if isinstance(payload, dict) else {}
                    if isinstance(detail, dict):
                        detail.setdefault("id", job_id)
                        detail.setdefault("canonicalPositionUrl", token)
                        row = _normalize(detail)
                        return [row] if row else []
                except (requests.RequestException, ValueError, RuntimeError, json.JSONDecodeError) as exc:
                    raise RuntimeError(f"Could not fetch Microsoft job detail {token}: {exc}") from exc
        elif token.startswith("http"):
            raise ValueError(f"Refusing non-Microsoft careers URL: {token}")

    print(f"[Microsoft] Starting public careers API scrape; page size={PAGE_SIZE}, max pages={MAX_PAGES}", flush=True)
    discovered = {}
    reported_total = None
    endpoint_used = None

    for page in range(MAX_PAGES):
        start = page * PAGE_SIZE
        rows, count, endpoint = _search_page(start)
        endpoint_used = endpoint
        if count is not None:
            try:
                reported_total = int(count)
            except (TypeError, ValueError):
                pass
        new_count = 0
        for item in rows:
            row = _normalize(item)
            if row:
                key = row["url"]
                if key not in discovered:
                    discovered[key] = item
                    new_count += 1
        print(
            f"[Microsoft] Page {page + 1}: {len(rows)} API rows, "
            f"{len(discovered)} unique normalized jobs"
            + (f" / {reported_total} reported" if reported_total is not None else ""),
            flush=True,
        )
        if not rows or new_count == 0:
            break
        if reported_total is not None and start + len(rows) >= reported_total:
            break
        # Classic Eightfold may return a short page before the true end; stop only
        # when the response is empty or it reports that we've reached its count.
    items = list(discovered.values())
    if FETCH_DETAILS and items:
        print(f"[Microsoft] Enriching {len(items)} jobs with detail endpoint", flush=True)
        enriched = {}
        with ThreadPoolExecutor(max_workers=DETAIL_WORKERS) as pool:
            futures = {pool.submit(_fetch_detail, item): item for item in items}
            for index, future in enumerate(as_completed(futures), 1):
                try:
                    item = future.result()
                    row = _normalize(item)
                    if row:
                        enriched[row["url"]] = row
                except Exception as exc:
                    print(f"[Microsoft] Detail parse failed: {exc}", flush=True)
                if index % 50 == 0 or index == len(futures):
                    print(f"[Microsoft] Details processed: {index}/{len(futures)}", flush=True)
        output = list(enriched.values())
    else:
        output = [row for item in items if (row := _normalize(item))]
    print(
        f"[Microsoft] Complete: {len(output)} jobs; endpoint={endpoint_used or 'none'}; "
        f"reported total={reported_total if reported_total is not None else 'unknown'}",
        flush=True,
    )
    return output
