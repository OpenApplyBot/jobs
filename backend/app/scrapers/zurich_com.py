"""Fast, bounded scraper for Zurich Insurance Group's official careers portal.

Uses the official careers listing and job detail pages. No browser, API key,
or generic auto-discovery retries. Returns OpenApplyBot's normalized schema.
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urlunparse, parse_qs

import requests

from .common import normalize, location_text

COMPANY_NAME = "Zurich Insurance"
CAREERS_URL = "https://www.careers.zurich.com/en"
OFFICIAL_DOMAIN = "zurich.com"
CSV_RANK = 333
TIMEOUT = (3.5, 6)
MAX_LIST_PAGES = 4
MAX_JOB_PAGES = 100
HEADERS = {
    "User-Agent": "OpenApplyBot-Jobs/1.0 (+https://github.com/OpenApplyBot/jobs; public job indexer)",
    "Accept": "text/html,application/xhtml+xml",
}


class _HTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.jsonld = []
        self._href = None
        self._anchor_text = []
        self._in_jsonld = False
        self._script_text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self._href, self._anchor_text = a["href"], []
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_jsonld, self._script_text = True, []

    def handle_data(self, data):
        if self._href is not None:
            self._anchor_text.append(data)
        if self._in_jsonld:
            self._script_text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(" ".join(self._anchor_text).split())))
            self._href, self._anchor_text = None, []
        elif tag == "script" and self._in_jsonld:
            self.jsonld.append("".join(self._script_text))
            self._in_jsonld, self._script_text = False, []


def _walk_jsonld(value):
    if isinstance(value, list):
        for item in value:
            yield from _walk_jsonld(item)
    elif isinstance(value, dict):
        typ = value.get("@type", [])
        if typ == "JobPosting" or (isinstance(typ, list) and "JobPosting" in typ):
            yield value
        for key in ("@graph", "mainEntity", "itemListElement"):
            if key in value:
                yield from _walk_jsonld(value[key])


def _official(url):
    p = urlparse(url)
    host = (p.hostname or "").lower()
    return p.scheme in ("http", "https") and (host == "zurich.com" or host.endswith(".zurich.com"))


def _canonical(url):
    p = urlparse(url)
    return urlunparse((p.scheme, p.netloc, p.path.rstrip("/"), "", p.query, ""))


def scrape(token: str | None = None):
    """Fetch and normalize current Zurich vacancies; failures are bounded and logged."""
    start = (token or "").strip() or CAREERS_URL
    if not _official(start):
        raise ValueError(f"Refusing non-Zurich careers URL: {start}")

    # The first URL is the global portal; the second is Zurich's official
    # early-careers board, which is useful when the main search is unavailable.
    seeds = [start]
    if start == CAREERS_URL:
        seeds.append("https://www.careers.zurich.com/go/Next-Generation-Careers/8578702/")

    session = requests.Session()
    session.headers.update(HEADERS)
    queue = list(dict.fromkeys(seeds))
    visited = set()
    job_links = {}
    records = {}

    while queue and len(visited) < MAX_LIST_PAGES:
        page = queue.pop(0)
        page = _canonical(page)
        if page in visited:
            continue
        visited.add(page)
        try:
            response = session.get(page, timeout=TIMEOUT, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as exc:
            print(f"[Zurich] Listing request failed ({page}): {exc}", flush=True)
            continue

        final_url = response.url
        if not _official(final_url):
            print(f"[Zurich] Ignoring off-domain redirect: {final_url}", flush=True)
            continue
        parser = _HTML()
        parser.feed(response.text)

        # Parse structured job records directly if the listing embeds them.
        for block in parser.jsonld:
            try:
                data = json.loads(block)
            except (ValueError, TypeError):
                continue
            for job in _walk_jsonld(data):
                row = _from_jsonld(job, final_url)
                if row:
                    records[row["source_job_id"]] = row

        for href, label in parser.links:
            absolute = _canonical(urljoin(final_url, href))
            if not _official(absolute):
                continue
            path = urlparse(absolute).path
            if re.search(r"/job/[^/]+/\d+", path, re.I):
                job_links.setdefault(absolute, label)
            elif "/go/" in path and absolute not in visited and absolute not in queue:
                # Only follow career listing pagination/category pages, not every site link.
                if len(queue) + len(visited) < MAX_LIST_PAGES and (
                    re.search(r"/\d+/?$", path) or "job" in path.lower() or "career" in path.lower()
                ):
                    queue.append(absolute)

    # Fetch individual official job pages for reliable descriptions and stable IDs.
    for url, link_title in list(job_links.items())[:MAX_JOB_PAGES]:
        try:
            response = session.get(url, timeout=TIMEOUT, allow_redirects=True)
            response.raise_for_status()
            if not _official(response.url):
                continue
        except requests.RequestException as exc:
            print(f"[Zurich] Job detail failed ({url}): {exc}", flush=True)
            continue

        parser = _HTML()
        parser.feed(response.text)
        found = False
        for block in parser.jsonld:
            try:
                data = json.loads(block)
            except (ValueError, TypeError):
                continue
            for job in _walk_jsonld(data):
                row = _from_jsonld(job, response.url, link_title)
                if row:
                    records[row["source_job_id"]] = row
                    found = True
        if not found and link_title:
            match = re.search(r"/(\d+)/?$", urlparse(response.url).path)
            if match:
                row = normalize(
                    match.group(1), link_title, response.url,
                    company=COMPANY_NAME, raw_payload={"source": "official Zurich careers page"},
                    apply_url=response.url,
                )
                if row:
                    records[row["source_job_id"]] = row

    output = list(records.values())
    print(f"[Zurich] Pages checked: {len(visited)}; job links: {len(job_links)}; jobs parsed: {len(output)}", flush=True)
    return output


def _from_jsonld(job, page_url, fallback_title=None):
    org = job.get("hiringOrganization") or {}
    if isinstance(org, list):
        org = org[0] if org else {}
    identifier = job.get("identifier") or {}
    if isinstance(identifier, dict):
        job_id = identifier.get("value") or identifier.get("name")
    else:
        job_id = identifier
    url = urljoin(page_url, job.get("url") or page_url)
    if not _official(url):
        url = page_url
    title = job.get("title") or fallback_title
    if not title:
        return None
    locations = job.get("jobLocation") or job.get("applicantLocationRequirements")
    description = job.get("description")
    if isinstance(description, dict):
        description = description.get("text") or description.get("html")
    if not job_id:
        match = re.search(r"/(\d+)/?$", urlparse(url).path)
        job_id = match.group(1) if match else url
    return normalize(
        str(job_id), title, url,
        location=location_text(locations),
        department=job.get("occupationalCategory") or job.get("industry"),
        employment_type=job.get("employmentType"),
        description=description,
        posted_at=job.get("datePosted"),
        company=(org.get("name") if isinstance(org, dict) else None) or COMPANY_NAME,
        raw_payload=job,
        apply_url=job.get("url") or url,
    )
