"""Company-specific scraper for BT Group.
Official careers URL candidate: https://bt.com/careers
Expected company domain: bt.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'BT Group'
CAREERS_URL = 'https://bt.com/careers'
OFFICIAL_DOMAIN = 'bt.com'
CSV_RANK = 448

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
