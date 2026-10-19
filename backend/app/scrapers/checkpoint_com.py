"""Company-specific scraper for Check Point.
Official careers URL candidate: https://checkpoint.com/careers
Expected company domain: checkpoint.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Check Point'
CAREERS_URL = 'https://checkpoint.com/careers'
OFFICIAL_DOMAIN = 'checkpoint.com'
CSV_RANK = 457

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
