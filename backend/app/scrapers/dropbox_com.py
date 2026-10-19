"""Company-specific scraper for Dropbox.
Official careers URL candidate: https://dropbox.com/careers
Expected company domain: dropbox.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Dropbox'
CAREERS_URL = 'https://dropbox.com/careers'
OFFICIAL_DOMAIN = 'dropbox.com'
CSV_RANK = 284

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
