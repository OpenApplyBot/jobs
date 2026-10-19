"""Company-specific scraper for Groww.
Official careers URL candidate: https://groww.in/careers
Expected company domain: groww.in
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Groww'
CAREERS_URL = 'https://groww.in/careers'
OFFICIAL_DOMAIN = 'groww.in'
CSV_RANK = 192

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
