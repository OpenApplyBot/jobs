"""Company-specific scraper for BNP Paribas.
Official careers URL candidate: https://bnpparibas.com/careers
Expected company domain: bnpparibas.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'BNP Paribas'
CAREERS_URL = 'https://bnpparibas.com/careers'
OFFICIAL_DOMAIN = 'bnpparibas.com'
CSV_RANK = 330

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
