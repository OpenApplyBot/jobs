"""Company-specific scraper for Reliance Retail.
Official careers URL candidate: https://ril.com/careers
Expected company domain: ril.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Reliance Retail'
CAREERS_URL = 'https://ril.com/careers'
OFFICIAL_DOMAIN = 'ril.com'
CSV_RANK = 219

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
