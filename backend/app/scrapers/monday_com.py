"""Company-specific scraper for Monday.com.
Official careers URL candidate: https://monday.com/careers
Expected company domain: monday.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Monday.com'
CAREERS_URL = 'https://monday.com/careers'
OFFICIAL_DOMAIN = 'monday.com'
CSV_RANK = 92

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
