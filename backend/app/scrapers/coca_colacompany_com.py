"""Company-specific scraper for Coca-Cola.
Official careers URL candidate: https://coca-colacompany.com/careers
Expected company domain: coca-colacompany.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Coca-Cola'
CAREERS_URL = 'https://coca-colacompany.com/careers'
OFFICIAL_DOMAIN = 'coca-colacompany.com'
CSV_RANK = 411

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
