"""Company-specific scraper for Merck.
Official careers URL candidate: https://merck.com/careers
Expected company domain: merck.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Merck'
CAREERS_URL = 'https://merck.com/careers'
OFFICIAL_DOMAIN = 'merck.com'
CSV_RANK = 393

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
