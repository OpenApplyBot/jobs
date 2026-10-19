"""Company-specific scraper for New Relic.
Official careers URL candidate: https://newrelic.com/careers
Expected company domain: newrelic.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'New Relic'
CAREERS_URL = 'https://newrelic.com/careers'
OFFICIAL_DOMAIN = 'newrelic.com'
CSV_RANK = 98

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
