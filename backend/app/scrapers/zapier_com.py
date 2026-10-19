"""Company-specific scraper for Zapier.
Official careers URL candidate: https://zapier.com/careers
Expected company domain: zapier.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zapier'
CAREERS_URL = 'https://zapier.com/careers'
OFFICIAL_DOMAIN = 'zapier.com'
CSV_RANK = 93

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
