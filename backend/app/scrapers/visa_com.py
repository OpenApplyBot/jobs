"""Company-specific scraper for Visa.
Official careers URL candidate: https://visa.com/careers
Expected company domain: visa.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Visa'
CAREERS_URL = 'https://visa.com/careers'
OFFICIAL_DOMAIN = 'visa.com'
CSV_RANK = 320

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
