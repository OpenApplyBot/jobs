"""Company-specific scraper for UPS.
Official careers URL candidate: https://ups.com/careers
Expected company domain: ups.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'UPS'
CAREERS_URL = 'https://ups.com/careers'
OFFICIAL_DOMAIN = 'ups.com'
CSV_RANK = 416

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
