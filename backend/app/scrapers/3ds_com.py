"""Company-specific scraper for Dassault Systèmes.
Official careers URL candidate: https://3ds.com/careers
Expected company domain: 3ds.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Dassault Systèmes'
CAREERS_URL = 'https://3ds.com/careers'
OFFICIAL_DOMAIN = '3ds.com'
CSV_RANK = 423

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
