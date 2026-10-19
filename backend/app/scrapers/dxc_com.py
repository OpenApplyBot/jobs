"""Company-specific scraper for DXC Technology.
Official careers URL candidate: https://dxc.com/careers
Expected company domain: dxc.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'DXC Technology'
CAREERS_URL = 'https://dxc.com/careers'
OFFICIAL_DOMAIN = 'dxc.com'
CSV_RANK = 160

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
