"""Company-specific scraper for Inditex.
Official job-listing URL: https://www.inditexpeople.com/us/en/joinus/offers
Expected company domain: inditex.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Inditex'
CAREERS_URL = 'https://www.inditexpeople.com/us/en/joinus/offers'
OFFICIAL_DOMAIN = 'inditex.com'
CSV_RANK = 406

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
