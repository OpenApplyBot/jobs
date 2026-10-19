"""Company-specific scraper for Northrop Grumman.
Official careers URL candidate: https://northropgrumman.com/careers
Expected company domain: northropgrumman.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Northrop Grumman'
CAREERS_URL = 'https://northropgrumman.com/careers'
OFFICIAL_DOMAIN = 'northropgrumman.com'
CSV_RANK = 371

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
