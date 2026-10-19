"""Company-specific scraper for Namecheap.
Official careers URL candidate: https://namecheap.com/careers
Expected company domain: namecheap.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Namecheap'
CAREERS_URL = 'https://namecheap.com/careers'
OFFICIAL_DOMAIN = 'namecheap.com'
CSV_RANK = 497

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
