"""Company-specific scraper for GE Vernova.
Official careers URL candidate: https://gevernova.com/careers
Expected company domain: gevernova.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'GE Vernova'
CAREERS_URL = 'https://gevernova.com/careers'
OFFICIAL_DOMAIN = 'gevernova.com'
CSV_RANK = 354

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
