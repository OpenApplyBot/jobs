"""Company-specific scraper for Instacart.
Official careers URL candidate: https://instacart.com/careers
Expected company domain: instacart.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Instacart'
CAREERS_URL = 'https://instacart.com/careers'
OFFICIAL_DOMAIN = 'instacart.com'
CSV_RANK = 260

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
