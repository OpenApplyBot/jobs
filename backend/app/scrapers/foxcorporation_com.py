"""Company-specific scraper for Fox Corporation.
Official careers URL candidate: https://foxcorporation.com/careers
Expected company domain: foxcorporation.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Fox Corporation'
CAREERS_URL = 'https://foxcorporation.com/careers'
OFFICIAL_DOMAIN = 'foxcorporation.com'
CSV_RANK = 480

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
