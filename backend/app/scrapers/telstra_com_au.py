"""Company-specific scraper for Telstra.
Official careers URL candidate: https://telstra.com.au/careers
Expected company domain: telstra.com.au
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Telstra'
CAREERS_URL = 'https://telstra.com.au/careers'
OFFICIAL_DOMAIN = 'telstra.com.au'
CSV_RANK = 445

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
