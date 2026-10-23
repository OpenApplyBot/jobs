"""Company-specific scraper for Carousell.
Official job-listing URL: https://careers.carousell.com/openings/
Expected company domain: carousell.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Carousell'
CAREERS_URL = 'https://careers.carousell.com/openings/'
OFFICIAL_DOMAIN = 'carousell.com'
CSV_RANK = 437

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
