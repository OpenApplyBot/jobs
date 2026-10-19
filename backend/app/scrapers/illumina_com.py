"""Company-specific scraper for Illumina.
Official careers URL candidate: https://illumina.com/careers
Expected company domain: illumina.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Illumina'
CAREERS_URL = 'https://illumina.com/careers'
OFFICIAL_DOMAIN = 'illumina.com'
CSV_RANK = 383

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
