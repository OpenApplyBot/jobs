"""Company-specific scraper for Philips.
Official careers URL candidate: https://philips.com/careers
Expected company domain: philips.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Philips'
CAREERS_URL = 'https://philips.com/careers'
OFFICIAL_DOMAIN = 'philips.com'
CSV_RANK = 380

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
