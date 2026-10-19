"""Company-specific scraper for Zerodha.
Official careers URL candidate: https://zerodha.com/careers
Expected company domain: zerodha.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zerodha'
CAREERS_URL = 'https://zerodha.com/careers'
OFFICIAL_DOMAIN = 'zerodha.com'
CSV_RANK = 193

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
