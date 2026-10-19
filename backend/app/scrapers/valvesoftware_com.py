"""Company-specific scraper for Valve.
Official careers URL candidate: https://valvesoftware.com/careers
Expected company domain: valvesoftware.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Valve'
CAREERS_URL = 'https://valvesoftware.com/careers'
OFFICIAL_DOMAIN = 'valvesoftware.com'
CSV_RANK = 280

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
