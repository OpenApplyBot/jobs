"""Company-specific scraper for Ford.
Official careers URL candidate: https://ford.com/careers
Expected company domain: ford.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Ford'
CAREERS_URL = 'https://ford.com/careers'
OFFICIAL_DOMAIN = 'ford.com'
CSV_RANK = 362

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
