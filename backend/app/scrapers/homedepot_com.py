"""Company-specific scraper for The Home Depot.
Official careers URL candidate: https://homedepot.com/careers
Expected company domain: homedepot.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'The Home Depot'
CAREERS_URL = 'https://homedepot.com/careers'
OFFICIAL_DOMAIN = 'homedepot.com'
CSV_RANK = 265

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
