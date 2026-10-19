"""Company-specific scraper for Expedia Group.
Official careers URL candidate: https://expediagroup.com/careers
Expected company domain: expediagroup.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Expedia Group'
CAREERS_URL = 'https://expediagroup.com/careers'
OFFICIAL_DOMAIN = 'expediagroup.com'
CSV_RANK = 267

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
