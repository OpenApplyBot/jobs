"""Company-specific scraper for ixigo.
Official careers URL candidate: https://ixigo.com/careers
Expected company domain: ixigo.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ixigo'
CAREERS_URL = 'https://ixigo.com/careers'
OFFICIAL_DOMAIN = 'ixigo.com'
CSV_RANK = 226

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
