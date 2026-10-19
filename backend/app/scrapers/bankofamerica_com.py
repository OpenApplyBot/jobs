"""Company-specific scraper for Bank of America.
Official careers URL candidate: https://bankofamerica.com/careers
Expected company domain: bankofamerica.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Bank of America'
CAREERS_URL = 'https://bankofamerica.com/careers'
OFFICIAL_DOMAIN = 'bankofamerica.com'
CSV_RANK = 324

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
