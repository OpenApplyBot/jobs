"""Company-specific scraper for Perfios.
Official careers URL candidate: https://perfios.com/careers
Expected company domain: perfios.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Perfios'
CAREERS_URL = 'https://perfios.com/careers'
OFFICIAL_DOMAIN = 'perfios.com'
CSV_RANK = 233

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
