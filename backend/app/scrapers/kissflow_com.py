"""Company-specific scraper for Kissflow.
Official careers URL candidate: https://kissflow.com/careers
Expected company domain: kissflow.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Kissflow'
CAREERS_URL = 'https://kissflow.com/careers'
OFFICIAL_DOMAIN = 'kissflow.com'
CSV_RANK = 171

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
