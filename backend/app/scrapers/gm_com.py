"""Company-specific scraper for General Motors.
Official careers URL candidate: https://gm.com/careers
Expected company domain: gm.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'General Motors'
CAREERS_URL = 'https://gm.com/careers'
OFFICIAL_DOMAIN = 'gm.com'
CSV_RANK = 363

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
