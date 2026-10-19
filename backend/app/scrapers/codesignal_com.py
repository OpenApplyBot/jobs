"""Company-specific scraper for CodeSignal.
Official careers URL candidate: https://codesignal.com/careers
Expected company domain: codesignal.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'CodeSignal'
CAREERS_URL = 'https://codesignal.com/careers'
OFFICIAL_DOMAIN = 'codesignal.com'
CSV_RANK = 306

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
