"""Company-specific scraper for AXA.
Official careers URL candidate: https://axa.com/careers
Expected company domain: axa.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'AXA'
CAREERS_URL = 'https://axa.com/careers'
OFFICIAL_DOMAIN = 'axa.com'
CSV_RANK = 334

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
