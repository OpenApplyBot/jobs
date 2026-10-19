"""Company-specific scraper for Mphasis.
Official careers URL candidate: https://mphasis.com/careers
Expected company domain: mphasis.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Mphasis'
CAREERS_URL = 'https://mphasis.com/careers'
OFFICIAL_DOMAIN = 'mphasis.com'
CSV_RANK = 144

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
