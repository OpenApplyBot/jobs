"""Company-specific scraper for Rapid7.
Official careers URL candidate: https://rapid7.com/careers
Expected company domain: rapid7.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Rapid7'
CAREERS_URL = 'https://rapid7.com/careers'
OFFICIAL_DOMAIN = 'rapid7.com'
CSV_RANK = 461

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
