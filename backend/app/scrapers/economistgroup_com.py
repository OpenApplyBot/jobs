"""Company-specific scraper for The Economist Group.
Official careers URL candidate: https://economistgroup.com/careers
Expected company domain: economistgroup.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'The Economist Group'
CAREERS_URL = 'https://economistgroup.com/careers'
OFFICIAL_DOMAIN = 'economistgroup.com'
CSV_RANK = 485

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
