"""Company-specific scraper for Unilever.
Official careers URL candidate: https://unilever.com/careers
Expected company domain: unilever.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Unilever'
CAREERS_URL = 'https://unilever.com/careers'
OFFICIAL_DOMAIN = 'unilever.com'
CSV_RANK = 409

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
