"""Company-specific scraper for Thermo Fisher Scientific.
Official careers URL candidate: https://thermofisher.com/careers
Expected company domain: thermofisher.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Thermo Fisher Scientific'
CAREERS_URL = 'https://thermofisher.com/careers'
OFFICIAL_DOMAIN = 'thermofisher.com'
CSV_RANK = 378

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
