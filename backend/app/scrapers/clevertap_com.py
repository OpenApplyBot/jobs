"""Company-specific scraper for CleverTap.
Official careers URL candidate: https://clevertap.com/careers
Expected company domain: clevertap.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'CleverTap'
CAREERS_URL = 'https://clevertap.com/careers'
OFFICIAL_DOMAIN = 'clevertap.com'
CSV_RANK = 251

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
