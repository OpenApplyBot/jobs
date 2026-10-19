"""Company-specific scraper for Trend Micro.
Official careers URL candidate: https://trendmicro.com/careers
Expected company domain: trendmicro.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Trend Micro'
CAREERS_URL = 'https://trendmicro.com/careers'
OFFICIAL_DOMAIN = 'trendmicro.com'
CSV_RANK = 456

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
