"""Company-specific scraper for HubSpot.
Official careers URL candidate: https://hubspot.com/careers
Expected company domain: hubspot.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'HubSpot'
CAREERS_URL = 'https://hubspot.com/careers'
OFFICIAL_DOMAIN = 'hubspot.com'
CSV_RANK = 286

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
