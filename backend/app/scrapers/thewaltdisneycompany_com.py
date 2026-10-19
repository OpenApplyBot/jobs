"""Company-specific scraper for The Walt Disney Company.
Official careers URL candidate: https://thewaltdisneycompany.com/careers
Expected company domain: thewaltdisneycompany.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'The Walt Disney Company'
CAREERS_URL = 'https://thewaltdisneycompany.com/careers'
OFFICIAL_DOMAIN = 'thewaltdisneycompany.com'
CSV_RANK = 476

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
