"""Salesforce Careers scraper for its public paginated jobs search."""
from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from urllib.parse import urljoin
import requests

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Salesforce"
CAREERS_URL = "https://careers.salesforce.com/en/jobs/"
OFFICIAL_DOMAIN = "careers.salesforce.com"
CSV_RANK = 23
PAGE_SIZE = max(1, min(100, int(os.getenv("SALESFORCE_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("SALESFORCE_MAX_PAGES", "20"))))

class _JobLinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active_href = None
        self.active_text = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            href = attrs.get("href", "")
            if re.match(r"^/en/jobs/[^/?#]+/[^?#]+", href):
                self.active_href = href
                self.active_text = []
    def handle_data(self, data):
        if self.active_href:
            self.active_text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.active_href:
            title = clean(" ".join(self.active_text))
            self.links.append((self.active_href, title))
            self.active_href = None
            self.active_text = []

def scrape(token: str | None = None):
    base_url = token.strip() if token and token.strip() else CAREERS_URL
    output, seen = [], set()
    with requests.Session() as session:
        session.headers.update({**HEADERS, "Accept": "text/html,application/xhtml+xml", "Referer": "https://careers.salesforce.com/"})
        for page in range(1, MAX_PAGES + 1):
            response = session.get(base_url, params={"page": page, "pagesize": PAGE_SIZE}, timeout=TIMEOUT)
            response.raise_for_status()
            parser = _JobLinkParser()
            parser.feed(response.text)
            added = 0
            for href, title in parser.links:
                job_url = urljoin(response.url, href)
                match = re.search(r"/en/jobs/([^/]+)/", href)
                job_id = clean(match.group(1)) if match else None
                if not job_id or not title or title.lower() in {"view job", "learn more"} or job_id in seen:
                    continue
                seen.add(job_id)
                item = normalize(job_id, title, job_url, company=COMPANY_NAME, raw_payload={"source": "Salesforce public careers HTML"}, apply_url=job_url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Salesforce] Page {page}: {added} job links, {len(output)} unique")
            if added == 0 or added < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Salesforce official jobs page yielded no parseable job links")
    print(f"[Salesforce] Complete: {len(output)} jobs")
    return output
