"""Company-specific scraper for Samsara.
Official careers URL candidate: https://samsara.com/careers
Expected company domain: samsara.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Samsara'
CAREERS_URL = 'https://samsara.com/careers'
OFFICIAL_DOMAIN = 'samsara.com'
CSV_RANK = 420

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
