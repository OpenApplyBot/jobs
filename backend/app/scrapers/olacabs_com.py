"""Company-specific scraper for Ola.
Official careers URL candidate: https://olacabs.com/careers
Expected company domain: olacabs.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Ola'
CAREERS_URL = 'https://olacabs.com/careers'
OFFICIAL_DOMAIN = 'olacabs.com'
CSV_RANK = 207

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
