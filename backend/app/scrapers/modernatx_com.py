"""Company-specific scraper for Moderna.
Official careers URL candidate: https://modernatx.com/careers
Expected company domain: modernatx.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Moderna'
CAREERS_URL = 'https://modernatx.com/careers'
OFFICIAL_DOMAIN = 'modernatx.com'
CSV_RANK = 384

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
