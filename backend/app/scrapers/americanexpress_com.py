"""Company-specific scraper for American Express.
Official careers URL candidate: https://americanexpress.com/careers
Expected company domain: americanexpress.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'American Express'
CAREERS_URL = 'https://americanexpress.com/careers'
OFFICIAL_DOMAIN = 'americanexpress.com'
CSV_RANK = 322

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
