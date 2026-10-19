"""Company-specific scraper for Fastly.
Official careers URL candidate: https://fastly.com/careers
Expected company domain: fastly.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Fastly'
CAREERS_URL = 'https://fastly.com/careers'
OFFICIAL_DOMAIN = 'fastly.com'
CSV_RANK = 76

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
