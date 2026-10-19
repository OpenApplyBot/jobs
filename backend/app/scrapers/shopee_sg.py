"""Company-specific scraper for Shopee.
Official careers URL candidate: https://shopee.sg/careers
Expected company domain: shopee.sg
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Shopee'
CAREERS_URL = 'https://shopee.sg/careers'
OFFICIAL_DOMAIN = 'shopee.sg'
CSV_RANK = 434

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
