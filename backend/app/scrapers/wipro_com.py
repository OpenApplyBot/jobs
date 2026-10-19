"""Company-specific scraper for Wipro.
Official careers URL candidate: https://careers.wipro.com/
Expected company domain: wipro.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Wipro'
CAREERS_URL = 'https://careers.wipro.com/'
OFFICIAL_DOMAIN = 'wipro.com'
CSV_RANK = 139

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
