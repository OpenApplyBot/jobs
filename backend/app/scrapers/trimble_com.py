"""Company-specific scraper for Trimble.
Official careers URL candidate: https://trimble.com/careers
Expected company domain: trimble.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Trimble'
CAREERS_URL = 'https://trimble.com/careers'
OFFICIAL_DOMAIN = 'trimble.com'
CSV_RANK = 421

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
