"""Company-specific scraper for UPS.
Official job-listing URL: https://www.jobs-ups.com/imea/en/search-results
Expected company domain: ups.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'UPS'
CAREERS_URL = 'https://www.jobs-ups.com/imea/en/search-results'
OFFICIAL_DOMAIN = 'ups.com'
CSV_RANK = 416

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
