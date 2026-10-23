"""Company-specific scraper for Orange.
Official job-listing URL: https://orange.jobs/gb/en/search-results
Expected company domain: orange.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Orange'
CAREERS_URL = 'https://orange.jobs/gb/en/search-results'
OFFICIAL_DOMAIN = 'orange.com'
CSV_RANK = 447

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
