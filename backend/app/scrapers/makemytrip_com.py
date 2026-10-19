"""Company-specific scraper for MakeMyTrip.
Official careers URL candidate: https://makemytrip.com/careers
Expected company domain: makemytrip.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'MakeMyTrip'
CAREERS_URL = 'https://makemytrip.com/careers'
OFFICIAL_DOMAIN = 'makemytrip.com'
CSV_RANK = 224

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
