"""Company-specific scraper for Jane Street.
Official careers URL candidate: https://janestreet.com/careers
Expected company domain: janestreet.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Jane Street'
CAREERS_URL = 'https://janestreet.com/careers'
OFFICIAL_DOMAIN = 'janestreet.com'
CSV_RANK = 132

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
