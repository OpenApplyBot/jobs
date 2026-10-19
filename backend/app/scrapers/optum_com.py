"""Company-specific scraper for Optum.
Official careers URL candidate: https://optum.com/careers
Expected company domain: optum.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Optum'
CAREERS_URL = 'https://optum.com/careers'
OFFICIAL_DOMAIN = 'optum.com'
CSV_RANK = 396

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
