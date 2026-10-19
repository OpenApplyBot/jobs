"""Company-specific scraper for Amplitude.
Official careers URL candidate: https://amplitude.com/careers
Expected company domain: amplitude.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Amplitude'
CAREERS_URL = 'https://amplitude.com/careers'
OFFICIAL_DOMAIN = 'amplitude.com'
CSV_RANK = 106

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
