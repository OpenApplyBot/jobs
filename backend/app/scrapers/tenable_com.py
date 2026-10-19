"""Company-specific scraper for Tenable.
Official careers URL candidate: https://tenable.com/careers
Expected company domain: tenable.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tenable'
CAREERS_URL = 'https://tenable.com/careers'
OFFICIAL_DOMAIN = 'tenable.com'
CSV_RANK = 460

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
