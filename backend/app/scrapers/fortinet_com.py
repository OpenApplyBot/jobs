"""Company-specific scraper for Fortinet.
Official careers URL candidate: https://fortinet.com/careers
Expected company domain: fortinet.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Fortinet'
CAREERS_URL = 'https://fortinet.com/careers'
OFFICIAL_DOMAIN = 'fortinet.com'
CSV_RANK = 293

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
