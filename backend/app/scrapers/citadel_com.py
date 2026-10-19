"""Company-specific scraper for Citadel.
Official careers URL candidate: https://citadel.com/careers
Expected company domain: citadel.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Citadel'
CAREERS_URL = 'https://citadel.com/careers'
OFFICIAL_DOMAIN = 'citadel.com'
CSV_RANK = 131

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
