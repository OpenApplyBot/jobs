"""Amazon Jobs scraper for the official amazon.jobs search and job-detail pages.

Uses the site's public JSON search representation first, with a public HTML
search-page fallback. No credentials or database access are required.
"""
from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs
import json
import os
import re

import requests

from .common import get, normalize, location_text, clean

COMPANY_NAME = "Amazon"
CAREERS_URL = "https://www.amazon.jobs/en/search"
SEARCH_JSON_URL = "https://www.amazon.jobs/en/search.json"
OFFICIAL_DOMAIN = "amazon.jobs"
CSV_RANK = 3

MAX_PAGES = max(1, int(os.getenv("AMAZON_MAX_PAGES", "100")))
PAGE_SIZE = max(1, min(100, int(os.getenv("AMAZON_PAGE_SIZE", "50"))))
FETCH_DETAILS = os.getenv("AMAZON_FETCH_DETAILS", "1").lower() not in {"0", "false", "no"}
TIMEOUT = max(5, int(os.getenv("AMAZON_HTTP_TIMEOUT", "20")))
HEADERS = {
    "User-Agent": "OpenApplyBot-Jobs/1.0 (+https://github.com/OpenApplyBot/jobs; public job indexer)",
    "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _get(url, params=None):
    response = get(url, params=params)
    host = (urlparse(response.url).hostname or "").lower()
    if host not in {"amazon.jobs", "www.amazon.jobs"}:
        raise ValueError(f"Unexpected redirect host for Amazon Jobs request: {host}")
    return response


def _text(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = re.sub(r"<[^>]+>", " ", value)
        return re.sub(r"\s+", " ", unescape(value)).strip() or None
    if isinstance(value, dict):
        for key in ("name", "label", "value", "text", "city", "location"):
            if value.get(key):
                return _text(value[key])
        return None
    if isinstance(value, list):
        return ", ".join(filter(None, (_text(part) for part in value))) or None
    return str(value)


def _first(item, *keys):
    for key in keys:
        value = item.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def _extract_jobs(payload):
    if isinstance(payload, list):
        return payload, None
    if not isinstance(payload, dict):
        return [], None
    for container in (payload, payload.get("data"), payload.get("results")):
        if isinstance(container, dict):
            for key in ("jobs", "search_results", "results", "hits", "items"):
                rows = container.get(key)
                if isinstance(rows, list):
                    total = _first(container, "total_hits", "total", "total_count", "count", "hits")
                    if isinstance(total, list):
                        total = len(total)
                    return rows, total
    return [], _first(payload, "total_hits", "total", "total_count", "count")


def _job_url(item):
    raw = _first(item, "job_path", "url", "job_url", "url_next_step", "job_url_path", "detail_url")
    if raw:
        url = urljoin("https://www.amazon.jobs/", str(raw))
        parsed = urlparse(url)
        if parsed.scheme == "https" and parsed.hostname in {"amazon.jobs", "www.amazon.jobs"}:
            return url
    job_id = _first(item, "id", "job_id", "jobId", "jobIdValue")
    slug = _first(item, "slug", "job_slug")
    if job_id:
        suffix = f"/{slug}" if slug else ""
        return f"https://www.amazon.jobs/en/jobs/{job_id}{suffix}"
    return None


def _job_id(item, url):
    value = _first(item, "id", "job_id", "jobId", "jobIdValue", "job_code", "jobCode")
    if value is not None:
        return str(value)
    match = re.search(r"/jobs/(\d+)", urlparse(url).path)
    if match:
        return match.group(1)
    query = parse_qs(urlparse(url).query)
    return (query.get("jobId") or [url])[0]


def _posted(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value / 1000 if value > 10_000_000_000 else value).isoformat()
        except (ValueError, OverflowError, OSError):
            return str(value)
    return str(value)


def _normalize(item):
    if not isinstance(item, dict):
        return None
    # Some result shapes wrap the original record in a search-hit envelope.
    if isinstance(item.get("_source"), dict):
        item = {**item["_source"], **{k: v for k, v in item.items() if k != "_source"}}
    url = _job_url(item)
    title = _text(_first(item, "title", "job_title", "jobTitle", "name", "display_title"))
    if not url or not title:
        return None
    location = _first(item, "location", "locations", "jobLocation", "normalized_location", "location_name", "city")
    if location is not None:
        location = location_text(location) or _text(location)
    department = _text(_first(item, "job_category", "category", "team", "business_category", "job_family"))
    employment_type = _text(_first(item, "job_type", "employment_type", "employmentType", "schedule_type", "type"))
    description = _first(item, "description", "job_description", "description_text", "basic_qualifications", "responsibilities")
    if isinstance(description, dict):
        description = _first(description, "text", "html", "value")
    job_id = _job_id(item, url)
    return normalize(
        job_id,
        title,
        url,
        location=location,
        department=department,
        employment_type=employment_type,
        description=description,
        posted_at=_posted(_first(item, "posted_date", "postedDate", "posted_at", "date_posted", "datePosted", "created_at")),
        company=COMPANY_NAME,
        raw_payload=item,
        apply_url=url,
    )


class _JobLinkParser(HTMLParser):
    """Small stdlib fallback parser for job links embedded in HTML search pages."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self._anchor = None
        self._inside_title = False
        self._jsonld = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._jsonld.append({"text": "", "active": True})
        elif tag == "a":
            href = attrs.get("href", "")
            if re.search(r"/en/jobs/\d+", href):
                self._anchor = {"url": urljoin("https://www.amazon.jobs/", href), "title": ""}
        elif self._anchor is not None and tag in {"h2", "h3"}:
            self._inside_title = True

    def handle_data(self, data):
        if self._jsonld and self._jsonld[-1].get("active"):
            self._jsonld[-1]["text"] += data
        if self._anchor is not None and (self._inside_title or not self._anchor["title"]):
            self._anchor["title"] += " " + data.strip()

    def handle_endtag(self, tag):
        if tag in {"h2", "h3"}:
            self._inside_title = False
        if tag == "a" and self._anchor is not None:
            title = clean(self._anchor["title"])
            if title:
                self.rows.append({"title": title, "url": self._anchor["url"]})
            self._anchor = None
        if tag == "script" and self._jsonld:
            self._jsonld[-1]["active"] = False


def _search_page(offset):
    params = {
        "base_query": "",
        "loc_query": "",
        "country": "",
        "offset": offset,
        "result_limit": PAGE_SIZE,
        "sort": "relevant",
    }
    errors = []
    try:
        response = _get(SEARCH_JSON_URL, params=params)
        payload = response.json()
        rows, total = _extract_jobs(payload)
        if rows:
            return rows, total, "json"
        errors.append(f"JSON endpoint returned no recognized job list (HTTP {response.status_code})")
    except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"JSON endpoint: {exc}")

    try:
        response = _get(CAREERS_URL, params={**params, "offset": offset})
        parser = _JobLinkParser()
        parser.feed(response.text)
        if parser.rows:
            return parser.rows, None, "html"
        # Some pages expose JSON-LD JobPosting objects without ordinary job cards.
        structured = []
        for block in parser._jsonld:
            try:
                data = json.loads(block["text"])
            except (ValueError, TypeError):
                continue
            values = data if isinstance(data, list) else [data]
            for obj in values:
                if isinstance(obj, dict) and obj.get("@type") == "JobPosting":
                    structured.append(obj)
        if structured:
            return structured, None, "html-jsonld"
        errors.append("HTML fallback contained no recognizable job links or JobPosting JSON-LD")
    except (requests.RequestException, ValueError) as exc:
        errors.append(f"HTML endpoint: {exc}")
    raise RuntimeError("Amazon Jobs search failed: " + " | ".join(errors))


def _detail_record(url):
    try:
        response = _get(url)
    except (requests.RequestException, ValueError) as exc:
        print(f"[Amazon] Detail fetch failed for {url}: {exc}", flush=True)
        return None
    parser = _JobLinkParser()
    parser.feed(response.text)
    for block in parser._jsonld:
        try:
            data = json.loads(block["text"])
        except (ValueError, TypeError):
            continue
        values = data if isinstance(data, list) else [data]
        for obj in values:
            if isinstance(obj, dict) and obj.get("@type") == "JobPosting":
                return obj
    # The listing record remains useful when the detail page has no JSON-LD.
    return None


def scrape(token: str | None = None):
    """Return normalized public Amazon Jobs listings; does not write to the DB."""
    token = (token or "").strip()
    if token:
        parsed = urlparse(token)
        if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"amazon.jobs", "www.amazon.jobs"}:
            raise ValueError(f"Refusing non-Amazon Jobs URL: {token}")
        detail = _detail_record(token)
        if detail:
            row = _normalize(detail)
            return [row] if row else []
        # If a specific job URL was requested but its schema is not parseable,
        # don't silently return the entire board.
        if re.search(r"/jobs/\d+", parsed.path):
            return []

    print(f"[Amazon] Starting official jobs search; page size={PAGE_SIZE}, max pages={MAX_PAGES}", flush=True)
    found = {}
    reported_total = None
    mode = None
    for page in range(MAX_PAGES):
        offset = page * PAGE_SIZE
        rows, total, page_mode = _search_page(offset)
        mode = page_mode
        try:
            if total is not None:
                reported_total = int(total)
        except (TypeError, ValueError):
            pass
        new_count = 0
        for item in rows:
            row = _normalize(item)
            if not row:
                continue
            if row["url"] not in found:
                found[row["url"]] = item
                new_count += 1
        print(
            f"[Amazon] Page {page + 1}: {len(rows)} source rows, "
            f"{len(found)} normalized unique jobs"
            + (f" / {reported_total} reported" if reported_total is not None else ""),
            flush=True,
        )
        if not rows or new_count == 0:
            break
        if reported_total is not None and offset + len(rows) >= reported_total:
            break
    records = [_normalize(item) for item in found.values()]
    records = [record for record in records if record]
    if FETCH_DETAILS and records:
        # Enrich only the first-page sample by default to avoid an unexpectedly
        # expensive N+1 crawl on the entire global job board.
        limit = min(len(records), PAGE_SIZE)
        print(f"[Amazon] Enriching first {limit} records with detail pages", flush=True)
        by_url = {row["url"]: row for row in records}
        for row in records[:limit]:
            detail = _detail_record(row["url"])
            if detail:
                enriched = _normalize(detail)
                if enriched:
                    by_url[row["url"]] = enriched
        records = list(by_url.values())
    print(f"[Amazon] Complete: {len(records)} jobs; mode={mode}; reported total={reported_total if reported_total is not None else 'unknown'}", flush=True)
    return records
