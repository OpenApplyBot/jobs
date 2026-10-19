"""Company-specific scraper for Zendesk.
Official careers URL candidate: https://zendesk.com/careers
Expected company domain: zendesk.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zendesk'
CAREERS_URL = 'https://zendesk.com/careers'
OFFICIAL_DOMAIN = 'zendesk.com'
CSV_RANK = 288

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
