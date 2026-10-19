"""Company-specific scraper for Panasonic.
Official careers URL candidate: https://panasonic.com/careers
Expected company domain: panasonic.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Panasonic'
CAREERS_URL = 'https://panasonic.com/careers'
OFFICIAL_DOMAIN = 'panasonic.com'
CSV_RANK = 19

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
