"""Company-specific scraper for HSBC.
Official careers URL candidate: https://hsbc.com/careers
Expected company domain: hsbc.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'HSBC'
CAREERS_URL = 'https://hsbc.com/careers'
OFFICIAL_DOMAIN = 'hsbc.com'
CSV_RANK = 327

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
