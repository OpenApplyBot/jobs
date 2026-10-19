"""Company-specific scraper for Brex.
Official careers URL candidate: https://brex.com/careers
Expected company domain: brex.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Brex'
CAREERS_URL = 'https://brex.com/careers'
OFFICIAL_DOMAIN = 'brex.com'
CSV_RANK = 118

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
