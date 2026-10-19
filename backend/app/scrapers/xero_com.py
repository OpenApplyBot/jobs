"""Company-specific scraper for Xero.
Official careers URL candidate: https://xero.com/careers
Expected company domain: xero.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Xero'
CAREERS_URL = 'https://xero.com/careers'
OFFICIAL_DOMAIN = 'xero.com'
CSV_RANK = 443

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
