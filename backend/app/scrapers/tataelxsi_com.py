"""Company-specific scraper for Tata Elxsi.
Official careers URL candidate: https://tataelxsi.com/careers
Expected company domain: tataelxsi.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tata Elxsi'
CAREERS_URL = 'https://tataelxsi.com/careers'
OFFICIAL_DOMAIN = 'tataelxsi.com'
CSV_RANK = 150

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
