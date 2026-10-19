"""Company-specific scraper for Upstox.
Official careers URL candidate: https://upstox.com/careers
Expected company domain: upstox.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Upstox'
CAREERS_URL = 'https://upstox.com/careers'
OFFICIAL_DOMAIN = 'upstox.com'
CSV_RANK = 194

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
