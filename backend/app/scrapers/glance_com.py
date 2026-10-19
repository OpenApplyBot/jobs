"""Company-specific scraper for Glance.
Official careers URL candidate: https://glance.com/careers
Expected company domain: glance.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Glance'
CAREERS_URL = 'https://glance.com/careers'
OFFICIAL_DOMAIN = 'glance.com'
CSV_RANK = 176

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
