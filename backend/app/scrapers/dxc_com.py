"""Company-specific scraper for DXC Technology.
Official careers URL candidate: https://careers.dxc.com/
Expected company domain: dxc.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'DXC Technology'
CAREERS_URL = 'https://careers.dxc.com/'
OFFICIAL_DOMAIN = 'dxc.com'
CSV_RANK = 160

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
