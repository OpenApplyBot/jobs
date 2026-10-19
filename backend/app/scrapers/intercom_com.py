"""Company-specific scraper for Intercom.
Official careers URL candidate: https://intercom.com/careers
Expected company domain: intercom.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Intercom'
CAREERS_URL = 'https://intercom.com/careers'
OFFICIAL_DOMAIN = 'intercom.com'
CSV_RANK = 287

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
