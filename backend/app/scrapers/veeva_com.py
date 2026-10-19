"""Company-specific scraper for Veeva Systems.
Official careers URL candidate: https://veeva.com/careers
Expected company domain: veeva.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Veeva Systems'
CAREERS_URL = 'https://veeva.com/careers'
OFFICIAL_DOMAIN = 'veeva.com'
CSV_RANK = 400

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
