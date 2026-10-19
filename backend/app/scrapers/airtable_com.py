"""Company-specific scraper for Airtable.
Official careers URL candidate: https://airtable.com/careers
Expected company domain: airtable.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Airtable'
CAREERS_URL = 'https://airtable.com/careers'
OFFICIAL_DOMAIN = 'airtable.com'
CSV_RANK = 88

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
