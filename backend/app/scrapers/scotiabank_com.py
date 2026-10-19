"""Company-specific scraper for Scotiabank.
Official careers URL candidate: https://scotiabank.com/careers
Expected company domain: scotiabank.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Scotiabank'
CAREERS_URL = 'https://scotiabank.com/careers'
OFFICIAL_DOMAIN = 'scotiabank.com'
CSV_RANK = 349

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
