"""Company-specific scraper for Boeing.
Official careers URL candidate: https://boeing.com/careers
Expected company domain: boeing.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Boeing'
CAREERS_URL = 'https://boeing.com/careers'
OFFICIAL_DOMAIN = 'boeing.com'
CSV_RANK = 369

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
