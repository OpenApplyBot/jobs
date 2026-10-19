"""Company-specific scraper for InMobi.
Official careers URL candidate: https://inmobi.com/careers
Expected company domain: inmobi.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'InMobi'
CAREERS_URL = 'https://inmobi.com/careers'
OFFICIAL_DOMAIN = 'inmobi.com'
CSV_RANK = 175

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
