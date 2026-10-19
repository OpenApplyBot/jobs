"""Company-specific scraper for Deloitte.
Official careers URL candidate: https://deloitte.com/careers
Expected company domain: deloitte.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Deloitte'
CAREERS_URL = 'https://deloitte.com/careers'
OFFICIAL_DOMAIN = 'deloitte.com'
CSV_RANK = 163

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
