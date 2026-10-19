"""Company-specific scraper for Tata 1mg.
Official careers URL candidate: https://1mg.com/careers
Expected company domain: 1mg.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tata 1mg'
CAREERS_URL = 'https://1mg.com/careers'
OFFICIAL_DOMAIN = '1mg.com'
CSV_RANK = 204

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
