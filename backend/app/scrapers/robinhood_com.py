"""Company-specific scraper for Robinhood.
Official careers URL candidate: https://robinhood.com/careers
Expected company domain: robinhood.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Robinhood'
CAREERS_URL = 'https://robinhood.com/careers'
OFFICIAL_DOMAIN = 'robinhood.com'
CSV_RANK = 121

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
