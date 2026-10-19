"""Company-specific scraper for TSMC.
Official careers URL candidate: https://tsmc.com/careers
Expected company domain: tsmc.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'TSMC'
CAREERS_URL = 'https://tsmc.com/careers'
OFFICIAL_DOMAIN = 'tsmc.com'
CSV_RANK = 40

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
