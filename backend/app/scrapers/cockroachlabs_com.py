"""Company-specific scraper for Cockroach Labs.
Official careers URL candidate: https://cockroachlabs.com/careers
Expected company domain: cockroachlabs.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cockroach Labs'
CAREERS_URL = 'https://cockroachlabs.com/careers'
OFFICIAL_DOMAIN = 'cockroachlabs.com'
CSV_RANK = 68

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
