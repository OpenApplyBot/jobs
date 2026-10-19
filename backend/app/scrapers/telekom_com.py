"""Company-specific scraper for Deutsche Telekom.
Official careers URL candidate: https://telekom.com/careers
Expected company domain: telekom.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Deutsche Telekom'
CAREERS_URL = 'https://telekom.com/careers'
OFFICIAL_DOMAIN = 'telekom.com'
CSV_RANK = 449

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
