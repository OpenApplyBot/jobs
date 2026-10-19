"""Company-specific scraper for MYOB.
Official careers URL candidate: https://myob.com/careers
Expected company domain: myob.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'MYOB'
CAREERS_URL = 'https://myob.com/careers'
OFFICIAL_DOMAIN = 'myob.com'
CSV_RANK = 444

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
