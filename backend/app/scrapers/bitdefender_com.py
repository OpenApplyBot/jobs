"""Company-specific scraper for Bitdefender.
Official careers URL candidate: https://bitdefender.com/careers
Expected company domain: bitdefender.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Bitdefender'
CAREERS_URL = 'https://bitdefender.com/careers'
OFFICIAL_DOMAIN = 'bitdefender.com'
CSV_RANK = 454

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
