"""Company-specific scraper for Pine Labs.
Official careers URL candidate: https://pinelabs.com/careers
Expected company domain: pinelabs.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Pine Labs'
CAREERS_URL = 'https://pinelabs.com/careers'
OFFICIAL_DOMAIN = 'pinelabs.com'
CSV_RANK = 188

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
