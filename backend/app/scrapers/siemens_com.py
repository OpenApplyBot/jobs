"""Company-specific scraper for Siemens.
Official careers URL candidate: https://siemens.com/careers
Expected company domain: siemens.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Siemens'
CAREERS_URL = 'https://siemens.com/careers'
OFFICIAL_DOMAIN = 'siemens.com'
CSV_RANK = 350

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
