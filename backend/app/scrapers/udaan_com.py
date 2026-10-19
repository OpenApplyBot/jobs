"""Company-specific scraper for Udaan.
Official careers URL candidate: https://udaan.com/careers
Expected company domain: udaan.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Udaan'
CAREERS_URL = 'https://udaan.com/careers'
OFFICIAL_DOMAIN = 'udaan.com'
CSV_RANK = 214

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
