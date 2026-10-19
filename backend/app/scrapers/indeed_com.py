"""Company-specific scraper for Indeed.
Official careers URL candidate: https://indeed.com/careers
Expected company domain: indeed.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Indeed'
CAREERS_URL = 'https://indeed.com/careers'
OFFICIAL_DOMAIN = 'indeed.com'
CSV_RANK = 318

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
