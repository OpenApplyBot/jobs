"""Company-specific scraper for Honeywell.
Official careers URL candidate: https://honeywell.com/careers
Expected company domain: honeywell.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Honeywell'
CAREERS_URL = 'https://honeywell.com/careers'
OFFICIAL_DOMAIN = 'honeywell.com'
CSV_RANK = 353

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
