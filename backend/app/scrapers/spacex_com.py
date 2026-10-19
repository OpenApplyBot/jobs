"""Company-specific scraper for SpaceX.
Official careers URL candidate: https://spacex.com/careers
Expected company domain: spacex.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'SpaceX'
CAREERS_URL = 'https://spacex.com/careers'
OFFICIAL_DOMAIN = 'spacex.com'
CSV_RANK = 366

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
