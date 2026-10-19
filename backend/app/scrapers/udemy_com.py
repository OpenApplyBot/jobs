"""Company-specific scraper for Udemy.
Official careers URL candidate: https://udemy.com/careers
Expected company domain: udemy.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Udemy'
CAREERS_URL = 'https://udemy.com/careers'
OFFICIAL_DOMAIN = 'udemy.com'
CSV_RANK = 310

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
