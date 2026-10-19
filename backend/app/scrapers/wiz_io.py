"""Company-specific scraper for Wiz.
Official careers URL candidate: https://wiz.io/careers
Expected company domain: wiz.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Wiz'
CAREERS_URL = 'https://wiz.io/careers'
OFFICIAL_DOMAIN = 'wiz.io'
CSV_RANK = 296

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
