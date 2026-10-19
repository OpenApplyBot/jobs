"""Company-specific scraper for Lenovo.
Official careers URL candidate: https://lenovo.com/careers
Expected company domain: lenovo.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Lenovo'
CAREERS_URL = 'https://lenovo.com/careers'
OFFICIAL_DOMAIN = 'lenovo.com'
CSV_RANK = 33

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
