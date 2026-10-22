"""Company-specific scraper for Unilever.
Official job-listing URL: https://careers.unilever.com/en/search-jobs
Expected company domain: unilever.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Unilever'
CAREERS_URL = 'https://careers.unilever.com/en/search-jobs'
OFFICIAL_DOMAIN = 'unilever.com'
CSV_RANK = 409

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
