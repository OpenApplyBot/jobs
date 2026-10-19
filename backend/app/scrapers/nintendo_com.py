"""Company-specific scraper for Nintendo.
Official careers URL candidate: https://nintendo.com/careers
Expected company domain: nintendo.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Nintendo'
CAREERS_URL = 'https://nintendo.com/careers'
OFFICIAL_DOMAIN = 'nintendo.com'
CSV_RANK = 279

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
