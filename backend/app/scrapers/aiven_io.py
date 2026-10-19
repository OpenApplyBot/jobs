"""Company-specific scraper for Aiven.
Official careers URL candidate: https://aiven.io/careers
Expected company domain: aiven.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Aiven'
CAREERS_URL = 'https://aiven.io/careers'
OFFICIAL_DOMAIN = 'aiven.io'
CSV_RANK = 302

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
