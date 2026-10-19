"""Company-specific scraper for Bloomberg.
Official careers URL candidate: https://bloomberg.com/careers
Expected company domain: bloomberg.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Bloomberg'
CAREERS_URL = 'https://bloomberg.com/careers'
OFFICIAL_DOMAIN = 'bloomberg.com'
CSV_RANK = 134

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
