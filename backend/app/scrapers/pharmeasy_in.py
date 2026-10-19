"""Company-specific scraper for PharmEasy.
Official careers URL candidate: https://pharmeasy.in/careers
Expected company domain: pharmeasy.in
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'PharmEasy'
CAREERS_URL = 'https://pharmeasy.in/careers'
OFFICIAL_DOMAIN = 'pharmeasy.in'
CSV_RANK = 203

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
