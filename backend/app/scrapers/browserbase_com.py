"""Company-specific scraper for Browserbase.
Official careers URL candidate: https://browserbase.com/careers
Expected company domain: browserbase.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Browserbase'
CAREERS_URL = 'https://browserbase.com/careers'
OFFICIAL_DOMAIN = 'browserbase.com'
CSV_RANK = 500

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
