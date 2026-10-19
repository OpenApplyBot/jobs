"""Company-specific scraper for Veeam.
Official careers URL candidate: https://careers.veeam.com/
Expected company domain: veeam.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Veeam'
CAREERS_URL = 'https://careers.veeam.com/'
OFFICIAL_DOMAIN = 'veeam.com'
CSV_RANK = 464

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
