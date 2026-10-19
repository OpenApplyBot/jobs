"""Zurich Insurance careers scraper.

Paginates the official /search results (25 jobs/page), then enriches each
listing from its official detail page. Returns OpenApplyBot's normalized schema.
No browser or third-party API credentials required.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urlunparse, urlencode, parse_qs
import json
import os
import re
import threading
import requests

from .common import normalize

COMPANY_NAME = "Zurich Insurance"
CAREERS_URL = "https://www.careers.zurich.com/search"
OFFICIAL_DOMAIN = "zurich.com"
CSV_RANK = 333

TIMEOUT = (4, 12)  # connect, read
PAGE_SIZE = 25
MAX_PAGES = max(1, int(os.getenv("ZURICH_MAX_PAGES", "100")))  # 100 covers 2,500 listings
DETAIL_WORKERS = max(1, min(12, int(os.getenv("ZURICH_DETAIL_WORKERS", "8"))))
FETCH_DETAILS = os.getenv("ZURICH_FETCH_DETAILS", "1").lower() not in {"0", "false", "no"}
USER_AGENT = (
    "OpenApplyBot-Jobs/1.0 (+https://github.com/OpenApplyBot/jobs; "
    "public job indexer)"
)
_thread_local = threading.local()


class _PageParser(HTMLParser):
    """Small stdlib HTML parser; no BeautifulSoup dependency."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.jsonld = []
        self.text = []
        self._href = None
        self._anchor = []
        self._script = False
        self._script_type = ""
        self._script_buf = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
        if tag == "a" and attrs.get("href"):
            self._href, self._anchor = attrs["href"], []
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._script, self._script_buf = True, []

    def handle_data(self, data):
        if not self._skip_depth:
            value = " ".join(data.split())
            if value:
                self.text.append(value)
            if self._href is not None:
                self._anchor.append(value)
        if self._script:
            self._script_buf.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._anchor).strip()))
            self._href, self._anchor = None, []
        if tag == "script":
            if self._script:
                self.jsonld.append("".join(self._script_buf))
                self._script = False
            if self._skip_depth:
                self._skip_depth -= 1
        elif tag in {"style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1


def _session():
    # requests.Session is not documented as thread-safe; one session per worker.
    if not hasattr(_thread_local, "session"):
        s = requests.Session()
        s.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        })
        _thread_local.session = s
    return _thread_local.session


def _official(url):
    p = urlparse(url)
    host = (p.hostname or "").lower()
    return p.scheme in {"http", "https"} and (host == "zurich.com" or host.endswith(".zurich.com"))


def _canonical(url):
    p = urlparse(url)
    return urlunparse((p.scheme, p.netloc, p.path.rstrip("/") + "/", "", "", ""))


def _fetch(url):
    response = _session().get(url, timeout=TIMEOUT, allow_redirects=True)
    response.raise_for_status()
    if not _official(response.url):
        raise ValueError(f"Unexpected off-domain redirect: {response.url}")
    parser = _PageParser()
    parser.feed(response.text)
    return response.url, parser


def _job_id(url):
    match = re.search(r"/(\d+)/?$", urlparse(url).path)
    return match.group(1) if match else url


def _listing_page_url(base, startrow):
    p = urlparse(base)
    params = parse_qs(p.query, keep_blank_values=True)
    params["startrow"] = [str(startrow)]
    params.setdefault("q", [""])
    params.setdefault("sortColumn", ["referencedate"])
    params.setdefault("sortDirection", ["desc"])
    return urlunparse((p.scheme, p.netloc, p.path or "/search", "", urlencode(params, doseq=True), ""))


def _parse_jobposting(parser, page_url):
    def walk(value):
        if isinstance(value, list):
            for item in value:
                yield from walk(item)
        elif isinstance(value, dict):
            typ = value.get("@type", [])
            if typ == "JobPosting" or (isinstance(typ, list) and "JobPosting" in typ):
                yield value
            for key in ("@graph", "mainEntity", "itemListElement"):
                if key in value:
                    yield from walk(value[key])

    for raw in parser.jsonld:
        try:
            payload = json.loads(raw)
        except (ValueError, TypeError):
            continue
        for job in walk(payload):
            yield job


def _clean(value):
    if value is None:
        return None
    if isinstance(value, list):
        return ", ".join(str(x) for x in value if x)
    if isinstance(value, dict):
        return value.get("name") or value.get("value") or value.get("text")
    return re.sub(r"\s+", " ", str(value)).strip() or None


def _from_jsonld(job, page_url, fallback_title=None):
    org = job.get("hiringOrganization") or {}
    ident = job.get("identifier") or {}
    jid = (ident.get("value") or ident.get("name")) if isinstance(ident, dict) else ident
    url = urljoin(page_url, job.get("url") or page_url)
    if not _official(url):
        url = page_url
    title = _clean(job.get("title")) or fallback_title
    if not title:
        return None
    loc = job.get("jobLocation") or job.get("applicantLocationRequirements")
    if isinstance(loc, list):
        loc = ", ".join(_location(x) for x in loc if _location(x))
    else:
        loc = _location(loc)
    desc = job.get("description")
    if isinstance(desc, dict):
        desc = desc.get("text") or desc.get("html")
    jid = jid or _job_id(url)
    return normalize(
        str(jid), title, url, location=loc,
        department=job.get("occupationalCategory") or job.get("industry"),
        employment_type=job.get("employmentType"), description=desc,
        posted_at=job.get("datePosted"),
        company=_clean(org) if not isinstance(org, dict) else org.get("name") or COMPANY_NAME,
        raw_payload=job, apply_url=url,
    )


def _location(value):
    if not value:
        return None
    if isinstance(value, list):
        return ", ".join(filter(None, (_location(v) for v in value)))
    if isinstance(value, dict):
        addr = value.get("address") or value
        if isinstance(addr, dict):
            parts = [addr.get(k) for k in ("addressLocality", "addressRegion", "addressCountry")]
            return ", ".join(str(p) for p in parts if p) or value.get("name")
        return value.get("name") or _location(addr)
    return str(value)


def _detail(url, listing):
    """Fetch and normalize one job detail page; returns None on per-job failure."""
    try:
        final_url, parser = _fetch(url)
    except (requests.RequestException, ValueError) as exc:
        print(f"[Zurich] detail failed: {url}: {exc}", flush=True)
        return None

    # Prefer official structured data; it carries the richest and least ambiguous fields.
    for job in _parse_jobposting(parser, final_url):
        row = _from_jsonld(job, final_url, listing.get("title"))
        if row:
            row["raw_payload"]["listing_metadata"] = {
                "job_area": listing.get("department"),
                "listing_location": listing.get("location"),
                "listing_date_posted": listing.get("posted_at"),
            }
            return row

    text = " ".join(parser.text)
    title = listing.get("title")
    # Jobvite-like Zurich detail pages expose a stable requisition number in the body.
    id_match = re.search(r"(?:Job\s*(?:ID|Number|Requisition)|Requisition\s*(?:ID|Number))\s*[:#]?\s*([A-Z0-9-]{4,})", text, re.I)
    job_id = id_match.group(1) if id_match else _job_id(final_url)
    location = listing.get("location")
    loc_match = re.search(r"Location\(s\)\s*:\s*(.+?)(?=\s+(?:Schedule|Recruiter name|Job type)\s*:|$)", text, re.I)
    if loc_match:
        location = loc_match.group(1).strip(" .")
    schedule = re.search(r"Schedule\s*:\s*([^|.]+?)(?=\s+(?:Recruiter name|Location\(s\))\s*:|$)", text, re.I)
    employment = schedule.group(1).strip() if schedule else None

    # Keep the visible page text as a description if no structured description exists.
    # Remove repeated navigation and footer noise by starting at Overview when present.
    overview = re.search(r"\bOverview\b\s+(.*?)(?=\s+(?:Location\(s\)|Schedule\s*:|Recruiter name\s*:|Find similar jobs:)|$)", text, re.I)
    description = overview.group(1).strip() if overview else None
    if description:
        description = description[:30000]

    raw = {
        "source": "Zurich official careers detail page",
        "job_id_from_url": _job_id(final_url),
        "job_area": listing.get("department"),
        "listing_location": listing.get("location"),
        "listing_date_posted": listing.get("posted_at"),
    }
    return normalize(
        job_id, title, final_url, location=location,
        department=listing.get("department"), employment_type=employment,
        description=description, posted_at=listing.get("posted_at"),
        company=COMPANY_NAME, raw_payload=raw, apply_url=final_url,
    )


def scrape(token: str | None = None):
    """Scrape Zurich's paginated official search results and normalize all records.

    Optional env vars:
      ZURICH_MAX_PAGES=100       maximum listing pages (25 jobs/page)
      ZURICH_DETAIL_WORKERS=8    concurrent detail fetches (1-12)
      ZURICH_FETCH_DETAILS=1     set 0 for fast listing-only mode
    """
    start = (token or "").strip() or CAREERS_URL
    if not _official(start):
        raise ValueError(f"Refusing non-Zurich URL: {start}")
    if "/job/" in urlparse(start).path.lower():
        _, parser = _fetch(start)
        title = next((label for href, label in parser.links if "apply" in label.lower()), None)
        row = next((_from_jsonld(job, start) for job in _parse_jobposting(parser, start)), None)
        return [row] if row else []

    print(f"[Zurich] Starting paginated scrape: {start}", flush=True)
    first_url = _listing_page_url(start, 0)
    try:
        _, first_parser = _fetch(first_url)
    except Exception as exc:
        print(f"[Zurich] First listing page failed: {exc}", flush=True)
        return []

    # Derive total count from the site's visible "Results 1 – 25 of N" text.
    first_text = " ".join(first_parser.text)
    total_match = re.search(r"Results\s+\d+\s*[–-]\s*\d+\s+of\s+(\d+)", first_text, re.I)
    total = int(total_match.group(1)) if total_match else None
    pages_by_count = (total + PAGE_SIZE - 1) // PAGE_SIZE if total else 1
    pages = min(MAX_PAGES, pages_by_count)
    print(f"[Zurich] Reported vacancies: {total if total is not None else 'unknown'}; listing pages to scan: {pages}", flush=True)

    listings = {}
    def collect(parser, page_url):
        for href, label in parser.links:
            absolute = urljoin(page_url, href)
            if not _official(absolute):
                continue
            path = urlparse(absolute).path
            if re.search(r"/job/[^/]+/\d+/?$", path, re.I):
                title = label.strip()
                if title and title.lower() not in {"apply now", "apply now »", "more"}:
                    listings.setdefault(_canonical(absolute), {
                        "title": title, "url": _canonical(absolute),
                        "department": None, "location": None, "posted_at": None,
                    })

    collect(first_parser, first_url)
    for page_no in range(1, pages):
        page_url = _listing_page_url(start, page_no * PAGE_SIZE)
        try:
            final_url, parser = _fetch(page_url)
            before = len(listings)
            collect(parser, final_url)
            print(f"[Zurich] Listing page {page_no + 1}/{pages}: {len(listings) - before} new jobs (total {len(listings)})", flush=True)
        except Exception as exc:
            print(f"[Zurich] Listing page {page_no + 1} failed: {exc}", flush=True)

    # The site renders listing metadata as table rows. Detail pages remain the
    # authoritative source for descriptions, requisition IDs and application URLs.
    if not FETCH_DETAILS:
        output = []
        for item in listings.values():
            row = normalize(
                _job_id(item["url"]), item["title"], item["url"],
                company=COMPANY_NAME, raw_payload={"source": "Zurich official paginated search"},
                apply_url=item["url"],
            )
            if row:
                output.append(row)
        print(f"[Zurich] Listing-only mode: {len(output)} jobs", flush=True)
        return output

    output = {}
    items = list(listings.values())
    print(f"[Zurich] Enriching {len(items)} job detail pages with {DETAIL_WORKERS} workers", flush=True)
    with ThreadPoolExecutor(max_workers=DETAIL_WORKERS) as pool:
        futures = {pool.submit(_detail, item["url"], item): item["url"] for item in items}
        for index, future in enumerate(as_completed(futures), 1):
            try:
                row = future.result()
                if row:
                    output[row["source_job_id"]] = row
            except Exception as exc:
                print(f"[Zurich] Unexpected detail error: {futures[future]}: {exc}", flush=True)
            if index % 50 == 0 or index == len(futures):
                print(f"[Zurich] Details processed: {index}/{len(futures)}; normalized jobs: {len(output)}", flush=True)

    print(f"[Zurich] Complete: {len(output)} normalized jobs from {len(listings)} listings", flush=True)
    return list(output.values())
