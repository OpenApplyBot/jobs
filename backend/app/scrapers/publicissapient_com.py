"""Publicis Sapient scraper using its current official careers portal.

The old publicissapient.com/careers URL was stale. Current public listings are
published on careers.publicissapient.com/job-search; generic discovery then
checks the live page for a public ATS feed or structured job data.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = "Publicis Sapient"
CAREERS_URL = "https://careers.publicissapient.com/job-search"
OFFICIAL_DOMAIN = "publicissapient.com"
CSV_RANK = 156


def scrape(token: str | None = None):
    """Fetch listings from the current official career-search page."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    return _auto_scrape(url)
