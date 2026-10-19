"""Company-specific scraper for Walmart Global Tech.
Official careers URL candidate: https://careers.walmart.com/technology
Expected company domain: walmart.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Walmart Global Tech'
CAREERS_URL = 'https://careers.walmart.com/technology'
OFFICIAL_DOMAIN = 'walmart.com'
CSV_RANK = 263

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
