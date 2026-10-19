"""Company-specific scraper for Gusto.
Official careers URL candidate: https://gusto.com/careers
Expected company domain: gusto.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Gusto'
CAREERS_URL = 'https://gusto.com/careers'
OFFICIAL_DOMAIN = 'gusto.com'
CSV_RANK = 316

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
