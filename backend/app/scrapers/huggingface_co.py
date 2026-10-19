"""Hugging Face scraper using its official public Workable careers page."""
from __future__ import annotations
import json
import os
from html.parser import HTMLParser
from urllib.parse import urljoin
import requests
from .common import HEADERS, TIMEOUT, clean, normalize, location_text

COMPANY_NAME = "Hugging Face"
CAREERS_URL = "https://apply.workable.com/huggingface/?not_found=true"
API_URL = "https://www.workable.com/api/accounts/huggingface?details=true"
OFFICIAL_DOMAIN = "apply.workable.com"
CSV_RANK = 56
MAX_JOBS = max(1, min(1000, int(os.getenv("HUGGINGFACE_MAX_JOBS", "200"))))

class _WorkablePage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.scripts = []
        self.href = None
        self.link_text = []
        self.script_type = None
        self.script_text = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            href = attrs.get("href", "")
            if "/huggingface/j/" in href:
                self.href = urljoin(CAREERS_URL, href)
                self.link_text = []
        if tag == "script":
            script_type = (attrs.get("type") or "").lower()
            script_id = (attrs.get("id") or "").lower()
            if "json" in script_type or "__next_data__" in script_id or "workable" in script_id:
                self.script_type = script_type or script_id
                self.script_text = []
    def handle_data(self, data):
        if self.href:
            self.link_text.append(data)
        if self.script_type:
            self.script_text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.href:
            self.links.append((self.href, clean(" ".join(self.link_text))))
            self.href = None
            self.link_text = []
        if tag == "script" and self.script_type:
            raw = "".join(self.script_text).strip()
            if raw:
                self.scripts.append(raw)
            self.script_type = None
            self.script_text = []

def _collect_json(value, output):
    if isinstance(value, dict):
        title = clean(value.get("title") or value.get("name"))
        shortcode = clean(value.get("shortcode") or value.get("id") or value.get("jobId"))
        url = clean(value.get("url") or value.get("application_url") or value.get("applyUrl"))
        if title and (shortcode or url) and any(k in value for k in ("shortcode", "application_url", "jobLocation", "location", "jobId", "datePosted")):
            output.append(value)
        for child in value.values():
            _collect_json(child, output)
    elif isinstance(value, list):
        for child in value:
            _collect_json(child, output)

def scrape(token: str | None = None):
    page_url = token.strip() if token and token.strip() else CAREERS_URL
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/json", "Accept-Language": "en-US,en;q=0.9", "Referer": "https://huggingface.co/"}
    with requests.Session() as session:
        response = session.get(page_url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        parser = _WorkablePage()
        parser.feed(response.text)
        rows = []
        seen = set()
        for url, title in parser.links:
            job_id = url.rstrip("/").rsplit("/", 1)[-1]
            if title and job_id not in seen:
                seen.add(job_id)
                rows.append({"shortcode": job_id, "title": title, "url": url})
        for raw in parser.scripts:
            try:
                payload = json.loads(raw)
            except (ValueError, TypeError):
                continue
            candidates = []
            _collect_json(payload, candidates)
            for row in candidates:
                job_id = clean(row.get("shortcode") or row.get("id") or row.get("jobId") or row.get("url"))
                title = clean(row.get("title") or row.get("name"))
                url = clean(row.get("url") or row.get("application_url") or row.get("applyUrl"))
                if not url and job_id:
                    url = f"https://apply.workable.com/huggingface/j/{job_id}/"
                if job_id and title and url and job_id not in seen:
                    seen.add(job_id)
                    rows.append(row | {"shortcode": job_id, "title": title, "url": url})
        if not rows:
            api_response = session.get(API_URL, headers={**headers, "Accept": "application/json"}, timeout=TIMEOUT)
            if api_response.ok:
                try:
                    api_payload = api_response.json()
                    api_rows = api_payload.get("jobs") or api_payload.get("results") or [] if isinstance(api_payload, dict) else []
                    if isinstance(api_rows, list):
                        rows.extend(x for x in api_rows if isinstance(x, dict))
                except ValueError:
                    pass
        output = []
        for row in rows:
            job_id = clean(row.get("shortcode") or row.get("id") or row.get("jobId") or row.get("url"))
            title = clean(row.get("title") or row.get("name"))
            url = clean(row.get("url") or row.get("application_url") or row.get("applyUrl"))
            if not url and job_id:
                url = f"https://apply.workable.com/huggingface/j/{job_id}/"
            if not job_id or not title or not url:
                continue
            location = row.get("location") or row.get("jobLocation")
            if isinstance(location, dict):
                address = location.get("address") or {}
                location = address.get("addressLocality") or address.get("addressRegion") or location.get("name")
            elif isinstance(location, list):
                location = location_text(location)
            if not location:
                location = ", ".join(filter(None, [clean(row.get("city")), clean(row.get("region")), clean(row.get("country"))])) or "Remote"
            item = normalize(job_id, title, url, clean(location), clean(row.get("department") or row.get("team")),
                             clean(row.get("employment_type") or row.get("employmentType")),
                             clean(row.get("description_short") or row.get("description")),
                             row.get("created_at") or row.get("datePosted"), COMPANY_NAME,
                             raw_payload=row, apply_url=url)
            if item:
                output.append(item)
            if len(output) >= MAX_JOBS:
                break
    if not output:
        raise RuntimeError("Hugging Face official Workable page exposed no parseable job postings")
    print(f"[Hugging Face] Official Workable page parsed {len(rows)} records; normalized jobs={len(output)}")
    return output
