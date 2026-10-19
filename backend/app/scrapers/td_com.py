"""Company-specific scraper for TD Bank.
Official careers URL candidate: https://td.com/careers
Expected company domain: td.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'TD Bank'
CAREERS_URL = 'https://td.com/careers'
OFFICIAL_DOMAIN = 'td.com'
CSV_RANK = 348

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
