"""Company-specific scraper for FedEx.
Official careers URL candidate: https://fedex.com/careers
Expected company domain: fedex.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'FedEx'
CAREERS_URL = 'https://fedex.com/careers'
OFFICIAL_DOMAIN = 'fedex.com'
CSV_RANK = 415

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
