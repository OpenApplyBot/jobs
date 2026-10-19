"""Company-specific scraper for VWO.
Official careers URL candidate: https://vwo.com/careers
Expected company domain: vwo.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'VWO'
CAREERS_URL = 'https://vwo.com/careers'
OFFICIAL_DOMAIN = 'vwo.com'
CSV_RANK = 248

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
