"""Company-specific scraper for GlobalLogic.
Official careers URL candidate: https://globallogic.com/careers
Expected company domain: globallogic.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'GlobalLogic'
CAREERS_URL = 'https://globallogic.com/careers'
OFFICIAL_DOMAIN = 'globallogic.com'
CSV_RANK = 153

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
