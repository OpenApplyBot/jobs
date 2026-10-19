"""Company-specific scraper for Vodafone.
Official careers URL candidate: https://vodafone.com/careers
Expected company domain: vodafone.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Vodafone'
CAREERS_URL = 'https://vodafone.com/careers'
OFFICIAL_DOMAIN = 'vodafone.com'
CSV_RANK = 446

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
