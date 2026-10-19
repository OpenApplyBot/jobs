"""Company-specific scraper for Cleartrip.
Official careers URL candidate: https://cleartrip.com/careers
Expected company domain: cleartrip.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cleartrip'
CAREERS_URL = 'https://cleartrip.com/careers'
OFFICIAL_DOMAIN = 'cleartrip.com'
CSV_RANK = 225

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
