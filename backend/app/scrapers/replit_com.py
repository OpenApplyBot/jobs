"""Company-specific scraper for Replit.
Official careers URL candidate: https://replit.com/careers
Expected company domain: replit.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Replit'
CAREERS_URL = 'https://replit.com/careers'
OFFICIAL_DOMAIN = 'replit.com'
CSV_RANK = 305

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
