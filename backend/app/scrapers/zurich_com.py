"""Company-specific scraper for Zurich Insurance.
Official careers URL candidate: https://zurich.com/careers
Expected company domain: zurich.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zurich Insurance'
CAREERS_URL = 'https://zurich.com/careers'
OFFICIAL_DOMAIN = 'zurich.com'
CSV_RANK = 333

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
