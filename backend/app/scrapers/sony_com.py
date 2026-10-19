"""Company-specific scraper for Sony.
Official careers URL candidate: https://sony.com/careers
Expected company domain: sony.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Sony'
CAREERS_URL = 'https://sony.com/careers'
OFFICIAL_DOMAIN = 'sony.com'
CSV_RANK = 18

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
