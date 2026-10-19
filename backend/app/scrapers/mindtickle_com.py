"""Company-specific scraper for Mindtickle.
Official careers URL candidate: https://mindtickle.com/careers
Expected company domain: mindtickle.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Mindtickle'
CAREERS_URL = 'https://mindtickle.com/careers'
OFFICIAL_DOMAIN = 'mindtickle.com'
CSV_RANK = 245

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
