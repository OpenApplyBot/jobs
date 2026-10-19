"""Company-specific scraper for Oracle.
Official careers URL candidate: https://careers.oracle.com/
Expected company domain: oracle.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Oracle'
CAREERS_URL = 'https://careers.oracle.com/'
OFFICIAL_DOMAIN = 'oracle.com'
CSV_RANK = 22

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
