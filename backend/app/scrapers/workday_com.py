"""Company-specific scraper for Workday.
Official careers URL candidate: https://workday.com/careers
Expected company domain: workday.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Workday'
CAREERS_URL = 'https://workday.com/careers'
OFFICIAL_DOMAIN = 'workday.com'
CSV_RANK = 281

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
