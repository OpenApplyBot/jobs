"""Company-specific scraper for Rivian.
Official careers URL candidate: https://rivian.com/careers
Expected company domain: rivian.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Rivian'
CAREERS_URL = 'https://rivian.com/careers'
OFFICIAL_DOMAIN = 'rivian.com'
CSV_RANK = 364

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
