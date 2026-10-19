"""Company-specific scraper for ClickUp.
Official careers URL candidate: https://clickup.com/careers
Expected company domain: clickup.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ClickUp'
CAREERS_URL = 'https://clickup.com/careers'
OFFICIAL_DOMAIN = 'clickup.com'
CSV_RANK = 90

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
