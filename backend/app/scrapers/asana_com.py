"""Company-specific scraper for Asana.
Official careers URL candidate: https://asana.com/careers
Expected company domain: asana.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Asana'
CAREERS_URL = 'https://asana.com/careers'
OFFICIAL_DOMAIN = 'asana.com'
CSV_RANK = 91

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
