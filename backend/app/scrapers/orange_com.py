"""Company-specific scraper for Orange.
Official careers URL candidate: https://orange.com/careers
Expected company domain: orange.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Orange'
CAREERS_URL = 'https://orange.com/careers'
OFFICIAL_DOMAIN = 'orange.com'
CSV_RANK = 447

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
