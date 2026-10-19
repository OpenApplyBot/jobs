"""Company-specific scraper for Unity.
Official careers URL candidate: https://unity.com/careers/positions
Expected company domain: unity.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Unity'
CAREERS_URL = 'https://unity.com/careers'
OFFICIAL_DOMAIN = 'unity.com'
CSV_RANK = 275

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
