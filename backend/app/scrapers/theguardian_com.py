"""Company-specific scraper for The Guardian.
Official careers URL candidate: https://theguardian.com/careers
Expected company domain: theguardian.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'The Guardian'
CAREERS_URL = 'https://theguardian.com/careers'
OFFICIAL_DOMAIN = 'theguardian.com'
CSV_RANK = 483

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
