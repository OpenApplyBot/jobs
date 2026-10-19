"""Company-specific scraper for Rippling.
Official careers URL candidate: https://rippling.com/careers
Expected company domain: rippling.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Rippling'
CAREERS_URL = 'https://rippling.com/careers'
OFFICIAL_DOMAIN = 'rippling.com'
CSV_RANK = 315

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
