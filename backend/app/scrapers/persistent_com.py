"""Company-specific scraper for Persistent Systems.
Official careers URL candidate: https://persistent.com/careers
Expected company domain: persistent.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Persistent Systems'
CAREERS_URL = 'https://persistent.com/careers'
OFFICIAL_DOMAIN = 'persistent.com'
CSV_RANK = 143

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
