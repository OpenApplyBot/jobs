"""Company-specific scraper for Mozilla.
Official careers URL candidate: https://mozilla.org/careers
Expected company domain: mozilla.org
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Mozilla'
CAREERS_URL = 'https://mozilla.org/careers'
OFFICIAL_DOMAIN = 'mozilla.org'
CSV_RANK = 491

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
