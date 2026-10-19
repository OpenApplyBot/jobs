"""Company-specific scraper for Kaspersky.
Official careers URL candidate: https://kaspersky.com/careers
Expected company domain: kaspersky.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Kaspersky'
CAREERS_URL = 'https://kaspersky.com/careers'
OFFICIAL_DOMAIN = 'kaspersky.com'
CSV_RANK = 453

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
