"""Company-specific scraper for Lyft.
Official careers URL candidate: https://lyft.com/careers
Expected company domain: lyft.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Lyft'
CAREERS_URL = 'https://lyft.com/careers'
OFFICIAL_DOMAIN = 'lyft.com'
CSV_RANK = 258

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
