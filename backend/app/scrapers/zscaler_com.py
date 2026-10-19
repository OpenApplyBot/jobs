"""Company-specific scraper for Zscaler.
Official careers URL candidate: https://zscaler.com/careers
Expected company domain: zscaler.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zscaler'
CAREERS_URL = 'https://zscaler.com/careers'
OFFICIAL_DOMAIN = 'zscaler.com'
CSV_RANK = 294

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
