"""Company-specific scraper for Allianz.
Official careers URL candidate: https://allianz.com/careers
Expected company domain: allianz.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Allianz'
CAREERS_URL = 'https://allianz.com/careers'
OFFICIAL_DOMAIN = 'allianz.com'
CSV_RANK = 332

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
