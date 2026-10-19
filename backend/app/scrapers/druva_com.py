"""Company-specific scraper for Druva.
Official careers URL candidate: https://druva.com/careers
Expected company domain: druva.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Druva'
CAREERS_URL = 'https://druva.com/careers'
OFFICIAL_DOMAIN = 'druva.com'
CSV_RANK = 172

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
