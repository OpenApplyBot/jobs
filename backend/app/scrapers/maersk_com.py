"""Company-specific scraper for Maersk.
Official careers URL candidate: https://maersk.com/careers
Expected company domain: maersk.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Maersk'
CAREERS_URL = 'https://maersk.com/careers'
OFFICIAL_DOMAIN = 'maersk.com'
CSV_RANK = 418

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
