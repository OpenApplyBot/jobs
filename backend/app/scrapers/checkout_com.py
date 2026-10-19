"""Company-specific scraper for Checkout.com.
Official careers URL candidate: https://checkout.com/careers
Expected company domain: checkout.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Checkout.com'
CAREERS_URL = 'https://checkout.com/careers'
OFFICIAL_DOMAIN = 'checkout.com'
CSV_RANK = 116

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
