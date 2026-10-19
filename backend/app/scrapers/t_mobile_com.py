"""Company-specific scraper for T-Mobile.
Official careers URL candidate: https://t-mobile.com/careers
Expected company domain: t-mobile.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'T-Mobile'
CAREERS_URL = 'https://t-mobile.com/careers'
OFFICIAL_DOMAIN = 't-mobile.com'
CSV_RANK = 473

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
