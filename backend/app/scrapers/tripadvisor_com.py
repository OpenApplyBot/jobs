"""Company-specific scraper for Tripadvisor.
Official careers URL candidate: https://tripadvisor.com/careers
Expected company domain: tripadvisor.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tripadvisor'
CAREERS_URL = 'https://tripadvisor.com/careers'
OFFICIAL_DOMAIN = 'tripadvisor.com'
CSV_RANK = 268

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
