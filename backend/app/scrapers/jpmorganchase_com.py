"""Company-specific scraper for JPMorgan Chase.
Official careers URL candidate: https://careers.jpmorgan.com/
Expected company domain: jpmorganchase.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'JPMorgan Chase'
CAREERS_URL = 'https://careers.jpmorgan.com/'
OFFICIAL_DOMAIN = 'jpmorganchase.com'
CSV_RANK = 128

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
