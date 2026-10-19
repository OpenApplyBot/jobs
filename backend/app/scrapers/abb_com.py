"""Company-specific scraper for ABB.
Official careers URL candidate: https://abb.com/careers
Expected company domain: abb.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ABB'
CAREERS_URL = 'https://abb.com/careers'
OFFICIAL_DOMAIN = 'abb.com'
CSV_RANK = 352

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
