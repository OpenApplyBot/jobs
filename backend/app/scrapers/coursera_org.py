"""Company-specific scraper for Coursera.
Official careers URL candidate: https://coursera.org/careers
Expected company domain: coursera.org
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Coursera'
CAREERS_URL = 'https://coursera.org/careers'
OFFICIAL_DOMAIN = 'coursera.org'
CSV_RANK = 307

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
