"""Company-specific scraper for Sentry.
Official careers URL candidate: https://sentry.io/careers
Expected company domain: sentry.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Sentry'
CAREERS_URL = 'https://sentry.io/careers'
OFFICIAL_DOMAIN = 'sentry.io'
CSV_RANK = 303

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
