"""Company-specific scraper for Verizon.
Official careers URL candidate: https://verizon.com/careers
Expected company domain: verizon.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Verizon'
CAREERS_URL = 'https://verizon.com/careers'
OFFICIAL_DOMAIN = 'verizon.com'
CSV_RANK = 472

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
