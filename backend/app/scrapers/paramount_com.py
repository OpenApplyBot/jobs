"""Company-specific scraper for Paramount.
Official careers URL candidate: https://paramount.com/careers
Expected company domain: paramount.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Paramount'
CAREERS_URL = 'https://paramount.com/careers'
OFFICIAL_DOMAIN = 'paramount.com'
CSV_RANK = 478

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
