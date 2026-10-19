"""Company-specific scraper for Adobe.
Official careers URL candidate: https://careers.adobe.com/
Expected company domain: adobe.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Adobe'
CAREERS_URL = 'https://careers.adobe.com/'
OFFICIAL_DOMAIN = 'adobe.com'
CSV_RANK = 24

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
