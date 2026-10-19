"""Company-specific scraper for ASOS.
Official careers URL candidate: https://asos.com/careers
Expected company domain: asos.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ASOS'
CAREERS_URL = 'https://asos.com/careers'
OFFICIAL_DOMAIN = 'asos.com'
CSV_RANK = 405

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
