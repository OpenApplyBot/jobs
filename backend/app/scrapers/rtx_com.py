"""Company-specific scraper for RTX.
Official careers URL candidate: https://rtx.com/careers
Expected company domain: rtx.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'RTX'
CAREERS_URL = 'https://rtx.com/careers'
OFFICIAL_DOMAIN = 'rtx.com'
CSV_RANK = 372

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
