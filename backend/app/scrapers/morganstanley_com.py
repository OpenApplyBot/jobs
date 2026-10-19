"""Company-specific scraper for Morgan Stanley.
Official careers URL candidate: https://morganstanley.com/careers
Expected company domain: morganstanley.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Morgan Stanley'
CAREERS_URL = 'https://morganstanley.com/careers'
OFFICIAL_DOMAIN = 'morganstanley.com'
CSV_RANK = 130

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
