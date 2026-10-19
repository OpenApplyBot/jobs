"""Company-specific scraper for Bentley Systems.
Official careers URL candidate: https://bentley.com/careers
Expected company domain: bentley.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Bentley Systems'
CAREERS_URL = 'https://bentley.com/careers'
OFFICIAL_DOMAIN = 'bentley.com'
CSV_RANK = 425

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
