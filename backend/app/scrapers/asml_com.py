"""Company-specific scraper for ASML.
Official careers URL candidate: https://asml.com/careers
Expected company domain: asml.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ASML'
CAREERS_URL = 'https://asml.com/careers'
OFFICIAL_DOMAIN = 'asml.com'
CSV_RANK = 39

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
