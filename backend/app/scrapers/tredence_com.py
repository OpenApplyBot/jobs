"""Company-specific scraper for Tredence.
Official careers URL candidate: https://tredence.com/careers
Expected company domain: tredence.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tredence'
CAREERS_URL = 'https://tredence.com/careers'
OFFICIAL_DOMAIN = 'tredence.com'
CSV_RANK = 241

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
