"""Company-specific scraper for Electronic Arts.
Official careers URL candidate: https://ea.com/careers
Expected company domain: ea.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Electronic Arts'
CAREERS_URL = 'https://ea.com/careers'
OFFICIAL_DOMAIN = 'ea.com'
CSV_RANK = 277

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
