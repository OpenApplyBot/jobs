"""Company-specific scraper for Mercari.
Official careers URL candidate: https://mercari.com/careers
Expected company domain: mercari.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Mercari'
CAREERS_URL = 'https://mercari.com/careers'
OFFICIAL_DOMAIN = 'mercari.com'
CSV_RANK = 442

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
