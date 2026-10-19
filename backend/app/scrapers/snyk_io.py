"""Company-specific scraper for Snyk.
Official careers URL candidate: https://snyk.io/careers
Expected company domain: snyk.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Snyk'
CAREERS_URL = 'https://snyk.io/careers'
OFFICIAL_DOMAIN = 'snyk.io'
CSV_RANK = 95

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
