"""Company-specific scraper for UBS.
Official careers URL candidate: https://ubs.com/careers
Expected company domain: ubs.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'UBS'
CAREERS_URL = 'https://ubs.com/careers'
OFFICIAL_DOMAIN = 'ubs.com'
CSV_RANK = 329

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
