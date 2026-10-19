"""Company-specific scraper for Epic Systems.
Official careers URL candidate: https://epic.com/careers
Expected company domain: epic.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Epic Systems'
CAREERS_URL = 'https://epic.com/careers'
OFFICIAL_DOMAIN = 'epic.com'
CSV_RANK = 399

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
