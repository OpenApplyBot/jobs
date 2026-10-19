"""Company-specific scraper for Airbnb.
Official careers URL candidate: https://careers.airbnb.com/
Expected company domain: airbnb.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Airbnb'
CAREERS_URL = 'https://careers.airbnb.com/'
OFFICIAL_DOMAIN = 'airbnb.com'
CSV_RANK = 257

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
