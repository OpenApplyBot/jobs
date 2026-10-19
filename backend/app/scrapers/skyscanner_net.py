"""Company-specific scraper for Skyscanner.
Official careers URL candidate: https://skyscanner.net/careers
Expected company domain: skyscanner.net
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Skyscanner'
CAREERS_URL = 'https://skyscanner.net/careers'
OFFICIAL_DOMAIN = 'skyscanner.net'
CSV_RANK = 269

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
