"""Company-specific scraper for Alibaba.
Official careers URL candidate: https://alibaba.com/careers
Expected company domain: alibaba.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Alibaba'
CAREERS_URL = 'https://alibaba.com/careers'
OFFICIAL_DOMAIN = 'alibaba.com'
CSV_RANK = 14

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
