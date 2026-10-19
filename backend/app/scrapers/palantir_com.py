"""Company-specific scraper for Palantir.
Official careers URL candidate: https://palantir.com/careers
Expected company domain: palantir.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Palantir'
CAREERS_URL = 'https://palantir.com/careers'
OFFICIAL_DOMAIN = 'palantir.com'
CSV_RANK = 52

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
