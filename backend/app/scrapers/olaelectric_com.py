"""Company-specific scraper for Ola Electric.
Official careers URL candidate: https://olaelectric.com/careers
Expected company domain: olaelectric.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Ola Electric'
CAREERS_URL = 'https://olaelectric.com/careers'
OFFICIAL_DOMAIN = 'olaelectric.com'
CSV_RANK = 208

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
