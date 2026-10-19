"""Company-specific scraper for Sourcegraph.
Official careers URL candidate: https://sourcegraph.com/careers
Expected company domain: sourcegraph.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Sourcegraph'
CAREERS_URL = 'https://sourcegraph.com/careers'
OFFICIAL_DOMAIN = 'sourcegraph.com'
CSV_RANK = 304

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
