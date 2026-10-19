"""Company-specific scraper for VerSe Innovation.
Official careers URL candidate: https://verse.in/careers
Expected company domain: verse.in
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'VerSe Innovation'
CAREERS_URL = 'https://verse.in/careers'
OFFICIAL_DOMAIN = 'verse.in'
CSV_RANK = 222

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
