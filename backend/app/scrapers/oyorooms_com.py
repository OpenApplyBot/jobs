"""Company-specific scraper for OYO.
Official careers URL candidate: https://oyorooms.com/careers
Expected company domain: oyorooms.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'OYO'
CAREERS_URL = 'https://oyorooms.com/careers'
OFFICIAL_DOMAIN = 'oyorooms.com'
CSV_RANK = 223

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
