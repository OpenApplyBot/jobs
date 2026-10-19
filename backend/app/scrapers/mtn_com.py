"""Company-specific scraper for MTN Group.
Official careers URL candidate: https://mtn.com/careers
Expected company domain: mtn.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'MTN Group'
CAREERS_URL = 'https://mtn.com/careers'
OFFICIAL_DOMAIN = 'mtn.com'
CSV_RANK = 450

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
