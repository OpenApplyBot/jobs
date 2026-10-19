"""Company-specific scraper for Volkswagen.
Official careers URL candidate: https://volkswagen-group.com/careers
Expected company domain: volkswagen-group.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Volkswagen'
CAREERS_URL = 'https://volkswagen-group.com/careers'
OFFICIAL_DOMAIN = 'volkswagen-group.com'
CSV_RANK = 360

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
