"""Company-specific scraper for Carousell.
Official careers URL candidate: https://carousell.com/careers
Expected company domain: carousell.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Carousell'
CAREERS_URL = 'https://carousell.com/careers'
OFFICIAL_DOMAIN = 'carousell.com'
CSV_RANK = 437

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
