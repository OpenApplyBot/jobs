"""Company-specific scraper for ESET.
Official careers URL candidate: https://eset.com/careers
Expected company domain: eset.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ESET'
CAREERS_URL = 'https://eset.com/careers'
OFFICIAL_DOMAIN = 'eset.com'
CSV_RANK = 455

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
