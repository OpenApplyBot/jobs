"""Company-specific scraper for Blue Origin.
Official careers URL candidate: https://blueorigin.com/careers
Expected company domain: blueorigin.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Blue Origin'
CAREERS_URL = 'https://blueorigin.com/careers'
OFFICIAL_DOMAIN = 'blueorigin.com'
CSV_RANK = 367

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
