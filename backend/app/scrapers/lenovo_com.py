"""Lenovo Careers scraper using the official Avature SearchJobs portal."""
from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import requests

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "Lenovo"
CAREERS_URL = "https://jobs.lenovo.com/en_US/careers/SearchJobs/"
OFFICIAL_DOMAIN = "jobs.lenovo.com"
CSV_RANK = 33
PAGE_SIZE = max(1, min(100, int(os.getenv("LENOVO_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("LENOVO_MAX_PAGES", "2"))))

class _AvatureLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.href = None
        self.text = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        absolute = urljoin("https://jobs.lenovo.com", href)
        if "/JobDetail/" in urlparse(absolute).path:
            self.href = absolute
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
        session.headers.update({**HEADERS, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml", "Referer": "https://jobs.lenovo.com/"})
        for page in range(MAX_PAGES):
            response = session.get(base_url, params={"jobOffset": page * PAGE_SIZE, "jobRecordsPerPage": PAGE_SIZE}, timeout=TIMEOUT)
            response.raise_for_status()
            parser = _AvatureLinks()
            parser.feed(response.text)
            added = 0
            for url, title in parser.links:
                path = urlparse(url).path
                match = re.search(r"/JobDetail/([^/?#]+)/([^/?#]+)", path, re.I)
                if not match:
                    continue
                job_id = clean(match.group(2))
                if not title:
                    title = clean(match.group(1).replace("-", " "))
                if not job_id or not title or title.lower() in {"view details", "apply now"} or job_id in seen:
                    continue
                seen.add(job_id)
                item = normalize(job_id, title, url, company=COMPANY_NAME,
                                 raw_payload={"source": "Lenovo public Avature careers HTML"}, apply_url=url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[Lenovo] Page {page + 1}: {added} job links, {len(output)} unique")
            if added == 0 or added < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("Lenovo official Avature portal yielded no parseable job links")
    print(f"[Lenovo] Complete: {len(output)} jobs")
    return output
