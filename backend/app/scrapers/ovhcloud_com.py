"""Company-specific scraper for OVHcloud.
Official careers URL candidate: https://ovhcloud.com/careers
Expected company domain: ovhcloud.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'OVHcloud'
CAREERS_URL = 'https://ovhcloud.com/careers'
OFFICIAL_DOMAIN = 'ovhcloud.com'
CSV_RANK = 298

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
