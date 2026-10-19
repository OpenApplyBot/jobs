"""Company-specific scraper for Bosch.
Official careers URL candidate: https://bosch.com/careers
Expected company domain: bosch.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Bosch'
CAREERS_URL = 'https://bosch.com/careers'
OFFICIAL_DOMAIN = 'bosch.com'
CSV_RANK = 356

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
