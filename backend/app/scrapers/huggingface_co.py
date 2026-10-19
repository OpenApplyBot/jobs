"""Hugging Face scraper using its official Workable careers page."""
from __future__ import annotations
import json
import os
import re
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin
import requests
from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "Hugging Face"
CAREERS_URL = "https://apply.workable.com/huggingface/"
API_URL = "https://apply.workable.com/api/v3/widget/accounts/huggingface"
OFFICIAL_DOMAIN = "apply.workable.com"
CSV_RANK = 56
MAX_JOBS = max(1, min(1000, int(os.getenv("HUGGINGFACE_MAX_JOBS", "200"))))

class _WorkableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self._href = None
        self._text = []
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        if re.search(r"/huggingface/j/[^/?#]+", href):
            self._href = urljoin(CAREERS_URL, href)
            self._text = []
    def handle_data(self, data):
        if self._href:
            self._text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self._href:
            self.links.append((self._href, clean(" ".join(self._text))))
            self._href = None
            self._text = []

def _from_json(value, out):
    if isinstance(value, dict):
        title = clean(value.get("title") or value.get("name"))
        shortcode = clean(value.get("shortcode") or value.get("id"))
        url = clean(value.get("url") or value.get("application_url"))
        if title and (shortcode or url) and any(k in value for k in ("shortcode", "application_url", "job", "location")):
            out.append(value)
        for child in value.values():
            _from_json(child, out)
    elif isinstance(value, list):
        for child in value:
            _from_json(child, out)

def _parse_page(html_text):
    rows, seen = [], set()
    parser = _WorkableParser()
    parser.feed(html_text)
    for url, title in parser.links:
        if not title:
            continue
        shortcode_match = re.search(r"/j/([^/?#]+)", url)
        job_id = shortcode_match.group(1) if shortcode_match else url
        if job_id not in seen:
            seen.add(job_id)
            rows.append({"shortcode": job_id, "title": title, "url": url})
    for match in re.finditer(r'<script[^>]*type=["\\']application/ld\\+json["\\'][^>]*>(.*?)</script>', html_text, re.I | re.S):
        try:
            value = json.loads(match.group(1).strip())
        except (ValueError, TypeError):
            continue
        values = value if isinstance(value, list) else [value]
        for row in values:
            if not isinstance(row, dict) or row.get("@type") != "JobPosting":
                continue
            job_id = clean((row.get("identifier") or {}).get("value") if isinstance(row.get("identifier"), dict) else row.get("identifier")) or clean(row.get("url"))
            if job_id and job_id not in seen:
                seen.add(job_id)
                rows.append({"shortcode": job_id, "title": row.get("title"), "url": row.get("url"),
                             "description": row.get("description"), "datePosted": row.get("datePosted"),
                             "jobLocation": row.get("jobLocation"), "employmentType": row.get("employmentType")})
    # Workable SSR payloads vary; walk JSON script blocks for job objects too.
    for match in re.finditer(r'<script[^>]*type=["\\']application/json["\\'][^>]*>(.*?)</script>', html_text, re.I | re.S):
        try:
            value = json.loads(match.group(1).strip())
        except (ValueError, TypeError):
            continue
        candidates = []
        _from_json(value, candidates)
        for row in candidates:
            job_id = clean(row.get("shortcode") or row.get("id") or row.get("url"))
            title = clean(row.get("title") or row.get("name"))
            url = clean(row.get("url") or row.get("application_url"))
            if not url and job_id:
                url = f"https://apply.workable.com/huggingface/j/{job_id}/"
            if job_id and title and url and job_id not in seen:
                seen.add(job_id)
                rows.append(row | {"shortcode": job_id, "title": title, "url": url})
    return rows

def scrape(token: str | None = None):
    output, seen = [], set()
    headers = {**HEADERS, "Accept": "text/html,application/xhtml+xml,application/json"}
    # The old Workable widget endpoint now returns 404; the official employer
    # page remains public and embeds the active postings.
    with requests.Session() as session:
        page = session.get(CAREERS_URL, headers=headers, timeout=TIMEOUT)
        if page.status_code >= 400:
            raise RuntimeError(f"Hugging Face official Workable page returned HTTP {page.status_code}")
        rows = _parse_page(page.text)
        if not rows:
            response = session.get(API_URL, headers={**headers, "Accept": "application/json"}, timeout=TIMEOUT)
            if response.ok:
                payload = response.json()
                rows = payload.get("jobs") or [] if isinstance(payload, dict) else []
        for row in rows:
            if not isinstance(row, dict):
                continue
            job_id = clean(row.get("shortcode") or row.get("id") or row.get("url"))
            title = clean(row.get("title") or row.get("name"))
            url = clean(row.get("url") or row.get("application_url"))
            if not url:
                shortcode = clean(row.get("shortcode"))
                if shortcode:
                    url = f"https://apply.workable.com/huggingface/j/{shortcode}/"
            if not job_id or not title or not url or job_id in seen:
                continue
            seen.add(job_id)
            location = row.get("location") or row.get("jobLocation")
            if isinstance(location, dict):
                address = location.get("address") or {}
                location = address.get("addressLocality") or address.get("addressRegion") or location.get("name")
            elif isinstance(location, list):
                location = location_text(location)
            if not location:
                location = ", ".join(filter(None, [clean(row.get("city")), clean(row.get("region")), clean(row.get("country"))])) or "Remote"
            description = clean(row.get("description_short") or row.get("description"))
            item = normalize(job_id, title, url, clean(location), clean(row.get("department") or row.get("team")),
                             clean(row.get("employment_type") or row.get("employmentType")), description,
                             row.get("created_at") or row.get("datePosted"), COMPANY_NAME,
                             raw_payload=row, apply_url=url)
            if item:
                output.append(item)
            if len(output) >= MAX_JOBS:
                break
    if not output:
        raise RuntimeError("Hugging Face official Workable page exposed no parseable job postings")
    print(f"[Hugging Face] Official Workable page rows={len(rows)}; normalized jobs={len(output)}")
    return output
