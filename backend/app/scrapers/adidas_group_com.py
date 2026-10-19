"""Company-specific scraper for Adidas.
Official careers URL candidate: https://adidas-group.com/careers
Expected company domain: adidas-group.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Adidas'
CAREERS_URL = 'https://adidas-group.com/careers'
OFFICIAL_DOMAIN = 'adidas-group.com'
CSV_RANK = 414

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
