"""Company-specific scraper for Wix.
Official careers URL candidate: https://wix.com/careers
Expected company domain: wix.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Wix'
CAREERS_URL = 'https://wix.com/careers'
OFFICIAL_DOMAIN = 'wix.com'
CSV_RANK = 495

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
