"""Oracle Careers scraper for its public Oracle Recruiting Cloud job search."""
from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import requests

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Oracle"
CAREERS_URL = "https://careers.oracle.com/en/sites/jobsearch/jobs?hl=en-IN"
OFFICIAL_DOMAIN = "careers.oracle.com"
CSV_RANK = 22
PAGE_SIZE = max(1, min(100, int(os.getenv("ORACLE_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("ORACLE_MAX_PAGES", "10"))))

class _OracleJobLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.href = None
        self.text = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        path = urlparse(urljoin("https://careers.oracle.com", href)).path
        if re.search(r"/(?:sites/jobsearch/job|job)/[^/?#]+", path, re.I):
            self.href = urljoin("https://careers.oracle.com", href)
            self.text = []
    def handle_data(self, data):
        if self.href:
            self.text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.href:
            self.links.append((self.href, clean(" ".join(self.text))))
            self.href = None
            self.text = []

def scrape(token: str | None = None):
    base_url = token.strip() if token and token.strip() else CAREERS_URL
    output, seen = [], set()
    with requests.Session() as session:
        session.headers.update({**HEADERS, "Accept": "text/html,application/xhtml+xml", "Referer": "https://careers.oracle.com/en/sites/jobsearch/"})
        for page in range(1, MAX_PAGES + 1):
            response = session.get(base_url, params={"page": page, "limit": PAGE_SIZE}, timeout=TIMEOUT)
            response.raise_for_status()
            parser = _OracleJobLinks()
            parser.feed(response.text)
            added = 0
            for url, title in parser.links:
                path = urlparse(url).path
                match = re.search(r"/(?:sites/jobsearch/job|job)/([^/?#]+)", path, re.I)
                job_id = clean(match.group(1)) if match else None
                if not job_id or not title or title.lower() in {"view job", "apply now", "learn more"} or job_id in seen:
                    continue
                seen.add(job_id)
                item = normalize(job_id, title, url, company=COMPANY_NAME,
                                 raw_payload={"source": "Oracle public careers HTML"}, apply_url=url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Oracle] Page {page}: {added} job links, {len(output)} unique")
            if added == 0 or added < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Oracle official careers page yielded no parseable job links")
    print(f"[Oracle] Complete: {len(output)} jobs")
    return output
