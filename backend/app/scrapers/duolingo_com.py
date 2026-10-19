"""Company-specific scraper for Duolingo.
Official careers URL candidate: https://duolingo.com/careers
Expected company domain: duolingo.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Duolingo'
CAREERS_URL = 'https://duolingo.com/careers'
OFFICIAL_DOMAIN = 'duolingo.com'
CSV_RANK = 308

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
