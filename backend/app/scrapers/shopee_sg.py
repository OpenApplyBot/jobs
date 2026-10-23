"""Company-specific scraper for Shopee.
Official job-listing URL: https://careers.shopee.sg/jobs?limit=50&offset=0
Expected company domain: shopee.sg
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Shopee'
CAREERS_URL = 'https://careers.shopee.sg/jobs?limit=50&offset=0'
OFFICIAL_DOMAIN = 'shopee.sg'
CSV_RANK = 434

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
