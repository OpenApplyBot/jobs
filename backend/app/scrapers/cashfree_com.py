"""Company-specific scraper for Cashfree Payments.
Official careers URL candidate: https://cashfree.com/careers
Expected company domain: cashfree.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cashfree Payments'
CAREERS_URL = 'https://cashfree.com/careers'
OFFICIAL_DOMAIN = 'cashfree.com'
CSV_RANK = 187

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
