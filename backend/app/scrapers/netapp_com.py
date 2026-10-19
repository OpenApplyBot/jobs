"""Company-specific scraper for NetApp.
Official careers URL candidate: https://netapp.com/careers
Expected company domain: netapp.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'NetApp'
CAREERS_URL = 'https://netapp.com/careers'
OFFICIAL_DOMAIN = 'netapp.com'
CSV_RANK = 469

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
