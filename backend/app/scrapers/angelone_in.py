"""Company-specific scraper for Angel One.
Official careers URL candidate: https://angelone.in/careers
Expected company domain: angelone.in
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Angel One'
CAREERS_URL = 'https://angelone.in/careers'
OFFICIAL_DOMAIN = 'angelone.in'
CSV_RANK = 195

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
