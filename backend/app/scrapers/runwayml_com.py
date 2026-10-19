"""Company-specific scraper for Runway.
Official careers URL candidate: https://runwayml.com/careers
Expected company domain: runwayml.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Runway'
CAREERS_URL = 'https://runwayml.com/careers'
OFFICIAL_DOMAIN = 'runwayml.com'
CSV_RANK = 58

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
