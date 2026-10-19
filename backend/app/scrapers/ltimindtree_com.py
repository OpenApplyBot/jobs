"""Company-specific scraper for LTIMindtree.
Official careers URL candidate: https://ltimindtree.com/careers
Expected company domain: ltimindtree.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'LTIMindtree'
CAREERS_URL = 'https://ltimindtree.com/careers'
OFFICIAL_DOMAIN = 'ltimindtree.com'
CSV_RANK = 142

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
