"""Company-specific scraper for The New York Times.
Official careers URL candidate: https://nytimes.com/careers
Expected company domain: nytimes.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'The New York Times'
CAREERS_URL = 'https://nytimes.com/careers'
OFFICIAL_DOMAIN = 'nytimes.com'
CSV_RANK = 481

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
