"""Company-specific scraper for NoBroker.
Official careers URL candidate: https://nobroker.in/careers
Expected company domain: nobroker.in
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'NoBroker'
CAREERS_URL = 'https://nobroker.in/careers'
OFFICIAL_DOMAIN = 'nobroker.in'
CSV_RANK = 211

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
