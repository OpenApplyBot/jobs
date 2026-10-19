"""Company-specific scraper for Qualys.
Official careers URL candidate: https://qualys.com/careers
Expected company domain: qualys.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Qualys'
CAREERS_URL = 'https://qualys.com/careers'
OFFICIAL_DOMAIN = 'qualys.com'
CSV_RANK = 462

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
