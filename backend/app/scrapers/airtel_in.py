"""Company-specific scraper for Airtel.
Official careers URL candidate: https://airtel.in/careers
Expected company domain: airtel.in
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Airtel'
CAREERS_URL = 'https://airtel.in/careers'
OFFICIAL_DOMAIN = 'airtel.in'
CSV_RANK = 220

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
