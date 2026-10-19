"""Company-specific scraper for Hexaware.
Official careers URL candidate: https://hexaware.com/careers
Expected company domain: hexaware.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Hexaware'
CAREERS_URL = 'https://hexaware.com/careers'
OFFICIAL_DOMAIN = 'hexaware.com'
CSV_RANK = 146

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
