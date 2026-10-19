"""Company-specific scraper for PTC.
Official careers URL candidate: https://ptc.com/careers
Expected company domain: ptc.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'PTC'
CAREERS_URL = 'https://ptc.com/careers'
OFFICIAL_DOMAIN = 'ptc.com'
CSV_RANK = 424

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
