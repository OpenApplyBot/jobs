"""Company-specific scraper for Birlasoft.
Official careers URL candidate: https://birlasoft.com/careers
Expected company domain: birlasoft.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Birlasoft'
CAREERS_URL = 'https://birlasoft.com/careers'
OFFICIAL_DOMAIN = 'birlasoft.com'
CSV_RANK = 147

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
