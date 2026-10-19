"""Company-specific scraper for Freshworks.
Official careers URL candidate: https://www.freshworks.com/company/careers/
Expected company domain: freshworks.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Freshworks'
CAREERS_URL = 'https://www.freshworks.com/company/careers/'
OFFICIAL_DOMAIN = 'freshworks.com'
CSV_RANK = 168

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
