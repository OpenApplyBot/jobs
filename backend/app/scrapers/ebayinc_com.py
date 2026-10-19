"""Company-specific scraper for eBay.
Official careers URL candidate: https://ebayinc.com/careers
Expected company domain: ebayinc.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'eBay'
CAREERS_URL = 'https://ebayinc.com/careers'
OFFICIAL_DOMAIN = 'ebayinc.com'
CSV_RANK = 261

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
