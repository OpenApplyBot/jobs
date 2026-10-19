"""Company-specific scraper for Citi.
Official careers URL candidate: https://citi.com/careers
Expected company domain: citi.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Citi'
CAREERS_URL = 'https://citi.com/careers'
OFFICIAL_DOMAIN = 'citi.com'
CSV_RANK = 346

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
