"""Company-specific scraper for Sanofi.
Official careers URL candidate: https://sanofi.com/careers
Expected company domain: sanofi.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Sanofi'
CAREERS_URL = 'https://sanofi.com/careers'
OFFICIAL_DOMAIN = 'sanofi.com'
CSV_RANK = 390

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
