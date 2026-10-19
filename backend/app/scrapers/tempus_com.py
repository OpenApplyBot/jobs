"""Company-specific scraper for Tempus AI.
Official careers URL candidate: https://tempus.com/careers
Expected company domain: tempus.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tempus AI'
CAREERS_URL = 'https://tempus.com/careers'
OFFICIAL_DOMAIN = 'tempus.com'
CSV_RANK = 401

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
