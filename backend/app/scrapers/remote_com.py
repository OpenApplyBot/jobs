"""Company-specific scraper for Remote.
Official careers URL candidate: https://remote.com/careers
Expected company domain: remote.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Remote'
CAREERS_URL = 'https://remote.com/careers'
OFFICIAL_DOMAIN = 'remote.com'
CSV_RANK = 314

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
