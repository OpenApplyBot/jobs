"""Company-specific scraper for BMW Group.
Official careers URL candidate: https://bmwgroup.com/careers
Expected company domain: bmwgroup.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'BMW Group'
CAREERS_URL = 'https://bmwgroup.com/careers'
OFFICIAL_DOMAIN = 'bmwgroup.com'
CSV_RANK = 358

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
