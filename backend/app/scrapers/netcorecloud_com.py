"""Company-specific scraper for Netcore Cloud.
Official careers URL candidate: https://netcorecloud.com/careers
Expected company domain: netcorecloud.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Netcore Cloud'
CAREERS_URL = 'https://netcorecloud.com/careers'
OFFICIAL_DOMAIN = 'netcorecloud.com'
CSV_RANK = 252

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
