"""Company-specific scraper for Smallcase.
Official careers URL candidate: https://smallcase.com/careers
Expected company domain: smallcase.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Smallcase'
CAREERS_URL = 'https://smallcase.com/careers'
OFFICIAL_DOMAIN = 'smallcase.com'
CSV_RANK = 231

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
