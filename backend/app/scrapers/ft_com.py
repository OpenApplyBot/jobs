"""Company-specific scraper for Financial Times.
Official careers URL candidate: https://ft.com/careers
Expected company domain: ft.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Financial Times'
CAREERS_URL = 'https://ft.com/careers'
OFFICIAL_DOMAIN = 'ft.com'
CSV_RANK = 484

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
