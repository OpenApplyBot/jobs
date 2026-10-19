"""Company-specific scraper for Signzy.
Official careers URL candidate: https://signzy.com/careers
Expected company domain: signzy.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Signzy'
CAREERS_URL = 'https://signzy.com/careers'
OFFICIAL_DOMAIN = 'signzy.com'
CSV_RANK = 234

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
