"""Company-specific scraper for Rakuten.
Official careers URL candidate: https://rakuten.com/careers
Expected company domain: rakuten.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Rakuten'
CAREERS_URL = 'https://rakuten.com/careers'
OFFICIAL_DOMAIN = 'rakuten.com'
CSV_RANK = 441

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
