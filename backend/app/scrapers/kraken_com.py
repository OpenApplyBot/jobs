"""Company-specific scraper for Kraken.
Official careers URL candidate: https://kraken.com/careers
Expected company domain: kraken.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Kraken'
CAREERS_URL = 'https://kraken.com/careers'
OFFICIAL_DOMAIN = 'kraken.com'
CSV_RANK = 123

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
