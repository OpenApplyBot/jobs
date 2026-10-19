"""Company-specific scraper for BigBasket.
Official careers URL candidate: https://bigbasket.com/careers
Expected company domain: bigbasket.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'BigBasket'
CAREERS_URL = 'https://bigbasket.com/careers'
OFFICIAL_DOMAIN = 'bigbasket.com'
CSV_RANK = 184

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
