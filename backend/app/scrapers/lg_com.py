"""Company-specific scraper for LG Electronics.
Official careers URL candidate: https://lg.com/careers
Expected company domain: lg.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'LG Electronics'
CAREERS_URL = 'https://lg.com/careers'
OFFICIAL_DOMAIN = 'lg.com'
CSV_RANK = 20

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
