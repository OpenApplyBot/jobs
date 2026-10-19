"""Company-specific scraper for Hostinger.
Official careers URL candidate: https://www.hostinger.com/career
Expected company domain: hostinger.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Hostinger'
CAREERS_URL = 'https://www.hostinger.com/career'
OFFICIAL_DOMAIN = 'hostinger.com'
CSV_RANK = 498

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
