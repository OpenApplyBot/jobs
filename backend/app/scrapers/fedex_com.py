"""Company-specific scraper for FedEx.
Official job-listing URL: https://careers.fedex.com/jobs
Expected company domain: fedex.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'FedEx'
CAREERS_URL = 'https://careers.fedex.com/jobs'
OFFICIAL_DOMAIN = 'fedex.com'
CSV_RANK = 415

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
