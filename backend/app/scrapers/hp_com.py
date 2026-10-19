"""HP Careers scraper using the public apply.hp.com search page."""
from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, parse_qs
import requests

from .common import HEADERS, TIMEOUT, clean, normalize

COMPANY_NAME = "HP"
CAREERS_URL = "https://apply.hp.com/careers/search?domain=hp.com&triggerGoButton=true"
OFFICIAL_DOMAIN = "apply.hp.com"
CSV_RANK = 31
PAGE_SIZE = max(1, min(100, int(os.getenv("HP_PAGE_SIZE", "20"))))
MAX_PAGES = max(1, min(100, int(os.getenv("HP_MAX_PAGES", "2"))))

class _HPJobLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.href = None
        self.text = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        absolute = urljoin("https://apply.hp.com", href)
        path = urlparse(absolute).path.lower()
        if "/careers/job/" in path or "/careers/jobs/" in path or "/job-detail/" in path:
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
        session.headers.update({**HEADERS, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml", "Referer": "https://apply.hp.com/careers"})
        for page in range(MAX_PAGES):
            response = session.get(base_url, params={"start": page * PAGE_SIZE, "triggerGoButton": "true"}, timeout=TIMEOUT)
            response.raise_for_status()
            parser = _HPJobLinks()
            parser.feed(response.text)
            added = 0
            for url, title in parser.links:
                parsed = urlparse(url)
                query = parse_qs(parsed.query)
                match = re.search(r"/(?:careers/jobs?|job-detail)/([^/?#]+)", parsed.path, re.I)
                job_id = clean((query.get("jobId") or query.get("requisitionId") or [None])[0] or (match.group(1) if match else None))
                if not job_id or not title or title.lower() in {"view job", "apply now", "learn more"} or job_id in seen:
                    continue
                seen.add(job_id)
                item = normalize(job_id, title, url, company=COMPANY_NAME,
                                 raw_payload={"source": "HP public careers HTML"}, apply_url=url)
                if item:
                    output.append(item)
                    added += 1
            print(f"[HP] Page {page + 1}: {added} job links, {len(output)} unique")
            if added == 0 or added < PAGE_SIZE:
                break
    if not output:
        raise RuntimeError("HP official careers page yielded no parseable job links")
    print(f"[HP] Complete: {len(output)} jobs")
    return output
