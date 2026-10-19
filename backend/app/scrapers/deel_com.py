"""Company-specific scraper for Deel.
Official careers URL candidate: https://deel.com/careers
Expected company domain: deel.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Deel'
CAREERS_URL = 'https://deel.com/careers'
OFFICIAL_DOMAIN = 'deel.com'
CSV_RANK = 313

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
