"""Company-specific scraper for Xero.
Official job-listing URL: https://careers.xero.com/jobs/?search=&origin=global
Expected company domain: xero.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Xero'
CAREERS_URL = 'https://careers.xero.com/jobs/?search=&origin=global'
OFFICIAL_DOMAIN = 'xero.com'
CSV_RANK = 443

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
