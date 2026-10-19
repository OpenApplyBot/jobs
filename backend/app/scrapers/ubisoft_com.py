"""Company-specific scraper for Ubisoft.
Official careers URL candidate: https://ubisoft.com/careers
Expected company domain: ubisoft.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Ubisoft'
CAREERS_URL = 'https://ubisoft.com/careers'
OFFICIAL_DOMAIN = 'ubisoft.com'
CSV_RANK = 278

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
