"""Company-specific scraper for Navi.
Official careers URL candidate: https://navi.com/careers
Expected company domain: navi.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Navi'
CAREERS_URL = 'https://navi.com/careers'
OFFICIAL_DOMAIN = 'navi.com'
CSV_RANK = 227

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
