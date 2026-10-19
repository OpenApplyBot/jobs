"""Company-specific scraper for Okta.
Official careers URL candidate: https://okta.com/careers
Expected company domain: okta.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Okta'
CAREERS_URL = 'https://okta.com/careers'
OFFICIAL_DOMAIN = 'okta.com'
CSV_RANK = 290

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
