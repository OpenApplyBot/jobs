"""Company-specific scraper for Lenskart.
Official careers URL candidate: https://lenskart.com/careers
Expected company domain: lenskart.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Lenskart'
CAREERS_URL = 'https://lenskart.com/careers'
OFFICIAL_DOMAIN = 'lenskart.com'
CSV_RANK = 206

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
