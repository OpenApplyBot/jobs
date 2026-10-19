"""Company-specific scraper for Linear.
Official careers URL candidate: https://linear.app/careers
Expected company domain: linear.app
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Linear'
CAREERS_URL = 'https://linear.app/careers'
OFFICIAL_DOMAIN = 'linear.app'
CSV_RANK = 87

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
