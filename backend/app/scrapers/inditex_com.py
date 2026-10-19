"""Company-specific scraper for Inditex.
Official careers URL candidate: https://inditex.com/careers
Expected company domain: inditex.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Inditex'
CAREERS_URL = 'https://inditex.com/careers'
OFFICIAL_DOMAIN = 'inditex.com'
CSV_RANK = 406

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
