"""Company-specific scraper for Scale AI.
Official careers URL candidate: https://scale.com/careers
Expected company domain: scale.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Scale AI'
CAREERS_URL = 'https://scale.com/careers'
OFFICIAL_DOMAIN = 'scale.com'
CSV_RANK = 53

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
