"""Company-specific scraper for Digit Insurance.
Official careers URL candidate: https://godigit.com/careers
Expected company domain: godigit.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Digit Insurance'
CAREERS_URL = 'https://godigit.com/careers'
OFFICIAL_DOMAIN = 'godigit.com'
CSV_RANK = 198

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
