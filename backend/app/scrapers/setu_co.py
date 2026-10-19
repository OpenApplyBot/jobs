"""Company-specific scraper for Setu.
Official careers URL candidate: https://setu.co/careers
Expected company domain: setu.co
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Setu'
CAREERS_URL = 'https://setu.co/careers'
OFFICIAL_DOMAIN = 'setu.co'
CSV_RANK = 232

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
