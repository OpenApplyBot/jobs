"""Company-specific scraper for Thoughtworks.
Official careers URL candidate: https://thoughtworks.com/careers
Expected company domain: thoughtworks.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Thoughtworks'
CAREERS_URL = 'https://thoughtworks.com/careers'
OFFICIAL_DOMAIN = 'thoughtworks.com'
CSV_RANK = 154

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
