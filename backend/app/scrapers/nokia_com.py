"""Company-specific scraper for Nokia.
Official careers URL candidate: https://nokia.com/careers
Expected company domain: nokia.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Nokia'
CAREERS_URL = 'https://nokia.com/careers'
OFFICIAL_DOMAIN = 'nokia.com'
CSV_RANK = 44

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
