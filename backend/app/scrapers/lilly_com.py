"""Company-specific scraper for Eli Lilly.
Official job-listing URL: https://careers.lilly.com/us/en/search-results
Expected company domain: lilly.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Eli Lilly'
CAREERS_URL = 'https://careers.lilly.com/us/en/search-results'
OFFICIAL_DOMAIN = 'lilly.com'
CSV_RANK = 392

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
