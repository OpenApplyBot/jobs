"""Company-specific scraper for Continental.
Official careers URL candidate: https://continental.com/careers
Expected company domain: continental.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Continental'
CAREERS_URL = 'https://continental.com/careers'
OFFICIAL_DOMAIN = 'continental.com'
CSV_RANK = 357

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
