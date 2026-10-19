"""Company-specific scraper for Algolia.
Official careers URL candidate: https://algolia.com/careers
Expected company domain: algolia.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Algolia'
CAREERS_URL = 'https://algolia.com/careers'
OFFICIAL_DOMAIN = 'algolia.com'
CSV_RANK = 108

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
