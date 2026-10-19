"""Company-specific scraper for Motorola Solutions.
Official careers URL candidate: https://motorolasolutions.com/careers
Expected company domain: motorolasolutions.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Motorola Solutions'
CAREERS_URL = 'https://motorolasolutions.com/careers'
OFFICIAL_DOMAIN = 'motorolasolutions.com'
CSV_RANK = 47

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
