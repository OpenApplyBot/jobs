"""Company-specific scraper for Mastercard.
Official careers URL candidate: https://mastercard.com/careers
Expected company domain: mastercard.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Mastercard'
CAREERS_URL = 'https://mastercard.com/careers'
OFFICIAL_DOMAIN = 'mastercard.com'
CSV_RANK = 321

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
