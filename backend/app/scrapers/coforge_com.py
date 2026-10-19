"""Company-specific scraper for Coforge.
Official careers URL candidate: https://coforge.com/careers
Expected company domain: coforge.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Coforge'
CAREERS_URL = 'https://coforge.com/careers'
OFFICIAL_DOMAIN = 'coforge.com'
CSV_RANK = 145

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
