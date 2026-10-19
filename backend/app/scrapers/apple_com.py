"""Scraper for Apple's server-rendered public job search results."""
from html.parser import HTMLParser
from urllib.parse import urljoin
import re

from .common import get, normalize

COMPANY_NAME = 'Apple'
CAREERS_URL = 'https://jobs.apple.com/en-us/search?location=united-states-USA'
OFFICIAL_DOMAIN = 'apple.com'
CSV_RANK = 4

class _AppleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.current = None
        self.capture = None
        self._parsed_items = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if tag == "a":
            href = attributes.get("href") or ""
            in_title = any(
                (item.get("id") or "").startswith("search-search-job-title-")
                for item in self.stack
            )
            if in_title and "/en-us/details/" in href and "/locationPicker" not in href:
                if self.current:
                    self._parsed_items.append(self.current)
                self.current = {
                    "href": href,
                    "title": [],
                    "team": [],
                    "posted_at": [],
                    "location": [],
                }
                self.capture = "title"
        elif self.current and tag == "span":
            if "team-name" in classes:
                self.capture = "team"
            elif "job-posted-date" in classes:
                self.capture = "posted_at"
            elif "table--advanced-search__location-sub" in classes:
                self.capture = "location"
        self.stack.append(attributes)

    def handle_data(self, data):
        if self.current and self.capture:
            self.current[self.capture].append(data)

    def handle_endtag(self, tag):
        if self.current and tag in {"a", "span"}:
            self.capture = None
        if self.stack:
            self.stack.pop()

    def jobs(self, base_url):
        jobs = []
        for item in self._items:
            match = re.search(r"/details/([^/?#]+)", item["href"])
            if not match:
                continue
            jobs.append(
                normalize(
                    match.group(1),
                    " ".join(item["title"]).strip(),
                    urljoin(base_url, item["href"]),
                    location=" ".join(item["location"]).strip(),
                    department=" ".join(item["team"]).strip(),
                    posted_at=" ".join(item["posted_at"]).strip(),
                    company="Apple",
                    raw_payload=item,
                    apply_url=urljoin(base_url, item["href"]),
                )
            )
        return [job for job in jobs if job]

    @property
    def _items(self):
        return getattr(self, "_parsed_items", [])

    def close(self):
        super().close()
        if self.current:
            self._parsed_items.append(self.current)
            self.current = None


def scrape(token: str | None = None):
    """Fetch jobs from an Apple search URL or the default US search page."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    response = get(url)
    parser = _AppleParser()
    parser.feed(response.text)
    parser.close()
    return parser.jobs(getattr(response, "url", None) or url)
