"""Company-specific scraper for Innovaccer.
Official careers URL candidate: https://innovaccer.com/careers
Expected company domain: innovaccer.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Innovaccer'
CAREERS_URL = 'https://innovaccer.com/careers'
OFFICIAL_DOMAIN = 'innovaccer.com'
CSV_RANK = 205

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
