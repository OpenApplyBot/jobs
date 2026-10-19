"""Company-specific scraper for HPE.
Official careers URL candidate: https://hpe.com/careers
Expected company domain: hpe.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'HPE'
CAREERS_URL = 'https://hpe.com/careers'
OFFICIAL_DOMAIN = 'hpe.com'
CSV_RANK = 32

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
