"""Company-specific scraper for Amagi.
Official careers URL candidate: https://amagi.com/careers
Expected company domain: amagi.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Amagi'
CAREERS_URL = 'https://amagi.com/careers'
OFFICIAL_DOMAIN = 'amagi.com'
CSV_RANK = 174

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
