"""Company-specific scraper for Arm.
Official careers URL candidate: https://arm.com/careers
Expected company domain: arm.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Arm'
CAREERS_URL = 'https://arm.com/careers'
OFFICIAL_DOMAIN = 'arm.com'
CSV_RANK = 34

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
