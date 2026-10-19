"""Company-specific scraper for L'Oréal.
Official careers URL candidate: https://loreal.com/careers
Expected company domain: loreal.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = "L'Oréal"
CAREERS_URL = 'https://loreal.com/careers'
OFFICIAL_DOMAIN = 'loreal.com'
CSV_RANK = 407

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
