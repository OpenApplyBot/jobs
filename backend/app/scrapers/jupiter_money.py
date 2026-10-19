"""Company-specific scraper for Jupiter.
Official careers URL candidate: https://jupiter.money/careers
Expected company domain: jupiter.money
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Jupiter'
CAREERS_URL = 'https://jupiter.money/careers'
OFFICIAL_DOMAIN = 'jupiter.money'
CSV_RANK = 229

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
