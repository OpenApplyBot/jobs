"""Company-specific scraper for Delhivery.
Official careers URL candidate: https://delhivery.com/careers
Expected company domain: delhivery.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Delhivery'
CAREERS_URL = 'https://delhivery.com/careers'
OFFICIAL_DOMAIN = 'delhivery.com'
CSV_RANK = 215

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
