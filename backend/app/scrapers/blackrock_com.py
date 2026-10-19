"""Company-specific scraper for BlackRock.
Official careers URL candidate: https://blackrock.com/careers
Expected company domain: blackrock.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'BlackRock'
CAREERS_URL = 'https://blackrock.com/careers'
OFFICIAL_DOMAIN = 'blackrock.com'
CSV_RANK = 341

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
