"""Company-specific scraper for Pfizer.
Official careers URL candidate: https://pfizer.com/careers
Expected company domain: pfizer.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Pfizer'
CAREERS_URL = 'https://pfizer.com/careers'
OFFICIAL_DOMAIN = 'pfizer.com'
CSV_RANK = 385

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
