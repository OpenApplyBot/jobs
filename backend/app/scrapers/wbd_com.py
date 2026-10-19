"""Company-specific scraper for Warner Bros. Discovery.
Official careers URL candidate: https://wbd.com/careers
Expected company domain: wbd.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Warner Bros. Discovery'
CAREERS_URL = 'https://wbd.com/careers'
OFFICIAL_DOMAIN = 'wbd.com'
CSV_RANK = 475

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
