"""Company-specific scraper for Cars24.
Official careers URL candidate: https://cars24.com/careers
Expected company domain: cars24.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cars24'
CAREERS_URL = 'https://cars24.com/careers'
OFFICIAL_DOMAIN = 'cars24.com'
CSV_RANK = 210

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
