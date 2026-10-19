"""Company-specific scraper for John Deere.
Official careers URL candidate: https://deere.com/careers
Expected company domain: deere.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'John Deere'
CAREERS_URL = 'https://deere.com/careers'
OFFICIAL_DOMAIN = 'deere.com'
CSV_RANK = 376

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
