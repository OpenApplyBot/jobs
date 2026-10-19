"""Company-specific scraper for Acko.
Official careers URL candidate: https://acko.com/careers
Expected company domain: acko.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Acko'
CAREERS_URL = 'https://acko.com/careers'
OFFICIAL_DOMAIN = 'acko.com'
CSV_RANK = 197

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
