"""Company-specific scraper for Dell Technologies.
Official careers URL candidate: https://dell.com/careers
Expected company domain: dell.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Dell Technologies'
CAREERS_URL = 'https://dell.com/careers'
OFFICIAL_DOMAIN = 'dell.com'
CSV_RANK = 30

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
