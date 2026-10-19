"""Company-specific scraper for Reddit.
Official careers URL candidate: https://redditinc.com/careers
Expected company domain: redditinc.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Reddit'
CAREERS_URL = 'https://redditinc.com/careers'
OFFICIAL_DOMAIN = 'redditinc.com'
CSV_RANK = 486

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
