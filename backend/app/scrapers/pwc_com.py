"""Company-specific scraper for PwC.
Official careers URL candidate: https://pwc.com/careers
Expected company domain: pwc.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'PwC'
CAREERS_URL = 'https://pwc.com/careers'
OFFICIAL_DOMAIN = 'pwc.com'
CSV_RANK = 164

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
