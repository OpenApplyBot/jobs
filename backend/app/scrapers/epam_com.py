"""Company-specific scraper for EPAM Systems.
Official careers URL candidate: https://epam.com/careers
Expected company domain: epam.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'EPAM Systems'
CAREERS_URL = 'https://epam.com/careers'
OFFICIAL_DOMAIN = 'epam.com'
CSV_RANK = 155

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
