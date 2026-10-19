"""Company-specific scraper for Juspay.
Official careers URL candidate: https://juspay.io/careers
Expected company domain: juspay.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Juspay'
CAREERS_URL = 'https://juspay.io/careers'
OFFICIAL_DOMAIN = 'juspay.io'
CSV_RANK = 185

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
