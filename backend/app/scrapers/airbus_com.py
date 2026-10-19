"""Company-specific scraper for Airbus.
Official careers URL candidate: https://airbus.com/careers
Expected company domain: airbus.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Airbus'
CAREERS_URL = 'https://airbus.com/careers'
OFFICIAL_DOMAIN = 'airbus.com'
CSV_RANK = 368

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
