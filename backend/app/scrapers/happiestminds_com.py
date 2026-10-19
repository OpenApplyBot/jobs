"""Company-specific scraper for Happiest Minds.
Official careers URL candidate: https://happiestminds.com/careers
Expected company domain: happiestminds.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Happiest Minds'
CAREERS_URL = 'https://happiestminds.com/careers'
OFFICIAL_DOMAIN = 'happiestminds.com'
CSV_RANK = 152

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
