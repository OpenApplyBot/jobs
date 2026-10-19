"""Company-specific scraper for KPMG.
Official careers URL candidate: https://kpmg.com/careers
Expected company domain: kpmg.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'KPMG'
CAREERS_URL = 'https://kpmg.com/careers'
OFFICIAL_DOMAIN = 'kpmg.com'
CSV_RANK = 166

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
