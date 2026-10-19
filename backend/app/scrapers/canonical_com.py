"""Company-specific scraper for Canonical.
Official careers URL candidate: https://canonical.com/careers
Expected company domain: canonical.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Canonical'
CAREERS_URL = 'https://canonical.com/careers'
OFFICIAL_DOMAIN = 'canonical.com'
CSV_RANK = 49

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
