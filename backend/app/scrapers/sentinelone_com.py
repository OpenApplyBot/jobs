"""Company-specific scraper for SentinelOne.
Official careers URL candidate: https://sentinelone.com/careers
Expected company domain: sentinelone.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'SentinelOne'
CAREERS_URL = 'https://sentinelone.com/careers'
OFFICIAL_DOMAIN = 'sentinelone.com'
CSV_RANK = 295

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
