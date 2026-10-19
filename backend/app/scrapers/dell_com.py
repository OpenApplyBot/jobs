"""Dell Technologies scraper using its official public careers search pages."""
from __future__ import annotations
import os
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, parse_qs
import requests
from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Dell Technologies"
CAREERS_URL = "https://enterpriseplatform.dell.com/hcmUI/CandidateExperience/en/sites/careers/jobs?source=pagebuilder_landingpage"
RADANCY_URL = "https://jobs.dell.com/en/search-jobs/india%20general/375/1/1"
OFFICIAL_DOMAIN = "dell.com"
CSV_RANK = 30
MAX_JOBS = max(1, min(1000, int(os.getenv("DELL_MAX_JOBS", "100"))))

class _JobLinks(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.links = []
        self.href = None
        self.text = []
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        absolute = urljoin(self.base, href)
        path = urlparse(absolute).path.lower()
        if re.search(r"/(?:job|jobs)/[^/?#]+", path) and not re.search(r"/sites/[^/]+/jobs/?$", path):
            self.href = absolute
            self.text = []
    def handle_data(self, data):
        if self.href:
            self.text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.href:
            title = clean(" ".join(self.text))
            self.links.append((self.href, title))
            self.href = None
            self.text = []

def _records(html_text, page_url):
    parser = _JobLinks(page_url)
    parser.feed(html_text)
    records, seen = [], set()
    for url, title in parser.links:
        if not title or len(title) < 4:
            continue
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        match = re.search(r"/(?:job|jobs)/([^/?#]+)", parsed.path, re.I)
        job_id = clean((query.get("jobId") or query.get("requisitionId") or [None])[0]) or (clean(match.group(1)) if match else None)
        if not job_id:
            job_id = clean(url)
        if job_id in seen:
            continue
        seen.add(job_id)
        item = normalize(job_id, title, url, company=COMPANY_NAME,
                         raw_payload={"source": "official Dell careers HTML"}, apply_url=url)
        if item:
            records.append(item)
    return records

def scrape(token: str | None = None):
    pages = [token.strip()] if token and token.strip() else [CAREERS_URL, RADANCY_URL]
    output, errors = [], []
    headers = {**HEADERS, "Accept": "text/html,application/xhtml+xml", "Referer": "https://www.dell.com/"}
    with requests.Session() as session:
        for page_url in pages:
            try:
                response = session.get(page_url, headers=headers, timeout=TIMEOUT)
                response.raise_for_status()
                rows = _records(response.text, response.url)
                print(f"[Dell Technologies] Official page {response.url}: parsed {len(rows)} job links")
                for row in rows:
                    if row["source_job_id"] not in {x["source_job_id"] for x in output}:
                        output.append(row)
                if len(output) >= MAX_JOBS:
                    break
            except Exception as exc:
                errors.append(f"{page_url}: {type(exc).__name__}: {exc}")
                print(f"[Dell Technologies] Page fallback failed: {errors[-1]}")
    if not output:
        raise RuntimeError("Dell official careers pages yielded no parseable job links; " + " | ".join(errors))
    print(f"[Dell Technologies] Complete: {len(output)} jobs")
    return output[:MAX_JOBS]
