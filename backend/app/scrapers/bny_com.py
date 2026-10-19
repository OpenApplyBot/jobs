"""Company-specific scraper for BNY.
Official careers URL candidate: https://bny.com/careers
Expected company domain: bny.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'BNY'
CAREERS_URL = 'https://bny.com/careers'
OFFICIAL_DOMAIN = 'bny.com'
CSV_RANK = 345

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
