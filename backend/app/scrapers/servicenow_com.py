"""Company-specific scraper for ServiceNow.
Official careers URL candidate: https://servicenow.com/careers
Expected company domain: servicenow.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ServiceNow'
CAREERS_URL = 'https://servicenow.com/careers'
OFFICIAL_DOMAIN = 'servicenow.com'
CSV_RANK = 282

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
