"""Company-specific scraper for Policybazaar.
Official careers URL candidate: https://policybazaar.com/careers
Expected company domain: policybazaar.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Policybazaar'
CAREERS_URL = 'https://policybazaar.com/careers'
OFFICIAL_DOMAIN = 'policybazaar.com'
CSV_RANK = 196

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
