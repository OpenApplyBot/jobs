"""Company-specific scraper for Nasdaq.
Official careers URL candidate: https://nasdaq.com/careers
Expected company domain: nasdaq.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Nasdaq'
CAREERS_URL = 'https://nasdaq.com/careers'
OFFICIAL_DOMAIN = 'nasdaq.com'
CSV_RANK = 340

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
