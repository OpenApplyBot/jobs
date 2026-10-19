"""Company-specific scraper for FIS.
Official careers URL candidate: https://fisglobal.com/careers
Expected company domain: fisglobal.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'FIS'
CAREERS_URL = 'https://fisglobal.com/careers'
OFFICIAL_DOMAIN = 'fisglobal.com'
CSV_RANK = 337

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
