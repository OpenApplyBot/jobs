"""Company-specific scraper for Intuit.
Official careers URL candidate: https://intuit.com/careers
Expected company domain: intuit.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Intuit'
CAREERS_URL = 'https://intuit.com/careers'
OFFICIAL_DOMAIN = 'intuit.com'
CSV_RANK = 335

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
