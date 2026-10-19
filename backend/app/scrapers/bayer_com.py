"""Company-specific scraper for Bayer.
Official careers URL candidate: https://bayer.com/careers
Expected company domain: bayer.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Bayer'
CAREERS_URL = 'https://bayer.com/careers'
OFFICIAL_DOMAIN = 'bayer.com'
CSV_RANK = 394

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
