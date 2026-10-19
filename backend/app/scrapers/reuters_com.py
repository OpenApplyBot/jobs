"""Company-specific scraper for Reuters.
Official careers URL candidate: https://reuters.com/careers
Expected company domain: reuters.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Reuters'
CAREERS_URL = 'https://reuters.com/careers'
OFFICIAL_DOMAIN = 'reuters.com'
CSV_RANK = 482

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
