"""Company-specific scraper for Zensar Technologies.
Official careers URL candidate: https://zensar.com/careers
Expected company domain: zensar.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zensar Technologies'
CAREERS_URL = 'https://zensar.com/careers'
OFFICIAL_DOMAIN = 'zensar.com'
CSV_RANK = 148

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
