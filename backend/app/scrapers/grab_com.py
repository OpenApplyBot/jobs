"""Company-specific scraper for Grab.
Official careers URL candidate: https://grab.com/careers
Expected company domain: grab.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Grab'
CAREERS_URL = 'https://grab.com/careers'
OFFICIAL_DOMAIN = 'grab.com'
CSV_RANK = 431

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
