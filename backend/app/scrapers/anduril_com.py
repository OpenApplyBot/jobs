"""Company-specific scraper for Anduril.
Official careers URL candidate: https://anduril.com/careers
Expected company domain: anduril.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Anduril'
CAREERS_URL = 'https://anduril.com/careers'
OFFICIAL_DOMAIN = 'anduril.com'
CSV_RANK = 63

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
