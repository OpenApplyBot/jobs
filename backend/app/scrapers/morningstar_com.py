"""Company-specific scraper for Morningstar.
Official careers URL candidate: https://morningstar.com/careers
Expected company domain: morningstar.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Morningstar'
CAREERS_URL = 'https://morningstar.com/careers'
OFFICIAL_DOMAIN = 'morningstar.com'
CSV_RANK = 136

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
