"""Company-specific scraper for Elastic.
Official careers URL candidate: https://elastic.co/careers
Expected company domain: elastic.co
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Elastic'
CAREERS_URL = 'https://elastic.co/careers'
OFFICIAL_DOMAIN = 'elastic.co'
CSV_RANK = 65

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
