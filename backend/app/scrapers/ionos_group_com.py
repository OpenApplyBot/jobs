"""Company-specific scraper for IONOS.
Official careers URL candidate: https://ionos-group.com/careers
Expected company domain: ionos-group.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'IONOS'
CAREERS_URL = 'https://ionos-group.com/careers'
OFFICIAL_DOMAIN = 'ionos-group.com'
CSV_RANK = 499

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
