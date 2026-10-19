"""Company-specific scraper for Deutsche Bank.
Official careers URL candidate: https://db.com/careers
Expected company domain: db.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Deutsche Bank'
CAREERS_URL = 'https://db.com/careers'
OFFICIAL_DOMAIN = 'db.com'
CSV_RANK = 328

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
