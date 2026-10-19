"""Company-specific scraper for Cyient.
Official careers URL candidate: https://cyient.com/careers
Expected company domain: cyient.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cyient'
CAREERS_URL = 'https://cyient.com/careers'
OFFICIAL_DOMAIN = 'cyient.com'
CSV_RANK = 151

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
