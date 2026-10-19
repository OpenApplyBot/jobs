"""Company-specific scraper for S&P Global.
Official careers URL candidate: https://spglobal.com/careers
Expected company domain: spglobal.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'S&P Global'
CAREERS_URL = 'https://spglobal.com/careers'
OFFICIAL_DOMAIN = 'spglobal.com'
CSV_RANK = 338

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
