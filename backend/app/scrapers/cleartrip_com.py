"""Company-specific scraper for Cleartrip.
Official careers URL candidate: https://careers.cleartrip.com/
Expected company domain: cleartrip.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cleartrip'
CAREERS_URL = 'https://careers.cleartrip.com/'
OFFICIAL_DOMAIN = 'cleartrip.com'
CSV_RANK = 225

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
