"""Company-specific scraper for Samsung Electronics.
Official careers URL candidate: https://samsung.com/careers
Expected company domain: samsung.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Samsung Electronics'
CAREERS_URL = 'https://samsung.com/careers'
OFFICIAL_DOMAIN = 'samsung.com'
CSV_RANK = 17

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
