"""Company-specific scraper for Swiggy.
Official careers URL candidate: https://careers.swiggy.com/
Expected company domain: swiggy.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Swiggy'
CAREERS_URL = 'https://careers.swiggy.com/'
OFFICIAL_DOMAIN = 'swiggy.com'
CSV_RANK = 181

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
