"""Company-specific scraper for OVHcloud.
Official careers URL candidate: https://careers.ovhcloud.com/en-in/
Expected company domain: ovhcloud.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'OVHcloud'
CAREERS_URL = 'https://careers.ovhcloud.com/en-in/'
OFFICIAL_DOMAIN = 'ovhcloud.com'
CSV_RANK = 298

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
