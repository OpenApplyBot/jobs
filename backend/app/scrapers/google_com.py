"""Company-specific scraper for Google.
Official careers URL candidate: https://www.google.com/about/careers/applications/
Expected company domain: google.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Google'
CAREERS_URL = 'https://www.google.com/about/careers/applications/'
OFFICIAL_DOMAIN = 'google.com'
CSV_RANK = 1

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
