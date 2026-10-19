"""Company-specific scraper for Ramp.
Official careers URL candidate: https://ramp.com/careers
Expected company domain: ramp.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Ramp'
CAREERS_URL = 'https://ramp.com/careers'
OFFICIAL_DOMAIN = 'ramp.com'
CSV_RANK = 119

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
