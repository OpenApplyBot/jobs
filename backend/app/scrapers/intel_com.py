"""Company-specific scraper for Intel.
Official careers URL candidate: https://intel.com/careers
Expected company domain: intel.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Intel'
CAREERS_URL = 'https://intel.com/careers'
OFFICIAL_DOMAIN = 'intel.com'
CSV_RANK = 27

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
