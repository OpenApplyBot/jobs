"""Company-specific scraper for Pure Storage.
Official careers URL candidate: https://purestorage.com/careers
Expected company domain: purestorage.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Pure Storage'
CAREERS_URL = 'https://purestorage.com/careers'
OFFICIAL_DOMAIN = 'purestorage.com'
CSV_RANK = 468

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
