"""Company-specific scraper for UnitedHealth Group.
Official careers URL candidate: https://unitedhealthgroup.com/careers
Expected company domain: unitedhealthgroup.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'UnitedHealth Group'
CAREERS_URL = 'https://unitedhealthgroup.com/careers'
OFFICIAL_DOMAIN = 'unitedhealthgroup.com'
CSV_RANK = 395

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
