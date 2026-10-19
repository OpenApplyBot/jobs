"""Company-specific scraper for Gojek.
Official careers URL candidate: https://gojek.io/careers
Expected company domain: gojek.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Gojek'
CAREERS_URL = 'https://gojek.io/careers'
OFFICIAL_DOMAIN = 'gojek.io'
CSV_RANK = 432

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
