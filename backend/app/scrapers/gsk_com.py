"""Company-specific scraper for GSK.
Official careers URL candidate: https://gsk.com/careers
Expected company domain: gsk.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'GSK'
CAREERS_URL = 'https://gsk.com/careers'
OFFICIAL_DOMAIN = 'gsk.com'
CSV_RANK = 389

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
