"""Company-specific scraper for Lockheed Martin.
Official careers URL candidate: https://lockheedmartin.com/careers
Expected company domain: lockheedmartin.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Lockheed Martin'
CAREERS_URL = 'https://lockheedmartin.com/careers'
OFFICIAL_DOMAIN = 'lockheedmartin.com'
CSV_RANK = 370

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
