"""Company-specific scraper for 3M.
Official careers URL candidate: https://3m.com/careers
Expected company domain: 3m.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = '3M'
CAREERS_URL = 'https://3m.com/careers'
OFFICIAL_DOMAIN = '3m.com'
CSV_RANK = 377

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
