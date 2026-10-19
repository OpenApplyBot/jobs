"""Company-specific scraper for F5.
Official careers URL candidate: https://f5.com/careers
Expected company domain: f5.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'F5'
CAREERS_URL = 'https://f5.com/careers'
OFFICIAL_DOMAIN = 'f5.com'
CSV_RANK = 470

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
