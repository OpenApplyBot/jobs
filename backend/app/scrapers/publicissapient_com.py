"""Company-specific scraper for Publicis Sapient.
Official careers URL candidate: https://publicissapient.com/careers
Expected company domain: publicissapient.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Publicis Sapient'
CAREERS_URL = 'https://publicissapient.com/careers'
OFFICIAL_DOMAIN = 'publicissapient.com'
CSV_RANK = 156

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
