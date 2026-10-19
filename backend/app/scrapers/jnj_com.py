"""Company-specific scraper for Johnson & Johnson.
Official careers URL candidate: https://jnj.com/careers
Expected company domain: jnj.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Johnson & Johnson'
CAREERS_URL = 'https://jnj.com/careers'
OFFICIAL_DOMAIN = 'jnj.com'
CSV_RANK = 391

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
