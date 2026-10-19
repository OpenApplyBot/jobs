"""Company-specific scraper for Uniphore.
Official careers URL candidate: https://uniphore.com/careers
Expected company domain: uniphore.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Uniphore'
CAREERS_URL = 'https://uniphore.com/careers'
OFFICIAL_DOMAIN = 'uniphore.com'
CSV_RANK = 255

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
