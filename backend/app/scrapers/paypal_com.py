"""Company-specific scraper for PayPal.
Official careers URL candidate: https://paypal.com/careers
Expected company domain: paypal.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'PayPal'
CAREERS_URL = 'https://paypal.com/careers'
OFFICIAL_DOMAIN = 'paypal.com'
CSV_RANK = 113

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
