"""Company-specific scraper for Cognizant.
Official careers URL candidate: https://cognizant.com/careers
Expected company domain: cognizant.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cognizant'
CAREERS_URL = 'https://cognizant.com/careers'
OFFICIAL_DOMAIN = 'cognizant.com'
CSV_RANK = 159

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
