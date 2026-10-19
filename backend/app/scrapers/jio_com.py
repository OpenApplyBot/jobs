"""Company-specific scraper for Jio Platforms.
Official careers URL candidate: https://jio.com/careers
Expected company domain: jio.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Jio Platforms'
CAREERS_URL = 'https://jio.com/careers'
OFFICIAL_DOMAIN = 'jio.com'
CSV_RANK = 218

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
