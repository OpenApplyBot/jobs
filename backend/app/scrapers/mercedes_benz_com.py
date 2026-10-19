"""Company-specific scraper for Mercedes-Benz.
Official careers URL candidate: https://mercedes-benz.com/careers
Expected company domain: mercedes-benz.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Mercedes-Benz'
CAREERS_URL = 'https://mercedes-benz.com/careers'
OFFICIAL_DOMAIN = 'mercedes-benz.com'
CSV_RANK = 359

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
