"""Company-specific scraper for Zalando.
Official careers URL candidate: https://zalando.com/careers
Expected company domain: zalando.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zalando'
CAREERS_URL = 'https://zalando.com/careers'
OFFICIAL_DOMAIN = 'zalando.com'
CSV_RANK = 404

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
