"""Company-specific scraper for Gupshup.
Official careers URL candidate: https://gupshup.io/careers
Expected company domain: gupshup.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Gupshup'
CAREERS_URL = 'https://gupshup.io/careers'
OFFICIAL_DOMAIN = 'gupshup.io'
CSV_RANK = 253

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
