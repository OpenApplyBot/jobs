"""Company-specific scraper for Wikimedia Foundation.
Official careers URL candidate: https://wikimediafoundation.org/careers
Expected company domain: wikimediafoundation.org
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Wikimedia Foundation'
CAREERS_URL = 'https://wikimediafoundation.org/careers'
OFFICIAL_DOMAIN = 'wikimediafoundation.org'
CSV_RANK = 492

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
