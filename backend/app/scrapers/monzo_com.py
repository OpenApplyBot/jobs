"""Company-specific scraper for Monzo.
Official careers URL candidate: https://monzo.com/careers
Expected company domain: monzo.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Monzo'
CAREERS_URL = 'https://monzo.com/careers'
OFFICIAL_DOMAIN = 'monzo.com'
CSV_RANK = 125

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
