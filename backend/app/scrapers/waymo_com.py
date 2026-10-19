"""Company-specific scraper for Waymo.
Official careers URL candidate: https://waymo.com/careers
Expected company domain: waymo.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Waymo'
CAREERS_URL = 'https://waymo.com/careers'
OFFICIAL_DOMAIN = 'waymo.com'
CSV_RANK = 62

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
