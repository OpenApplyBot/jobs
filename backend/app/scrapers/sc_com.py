"""Company-specific scraper for Standard Chartered.
Official careers URL candidate: https://sc.com/careers
Expected company domain: sc.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Standard Chartered'
CAREERS_URL = 'https://sc.com/careers'
OFFICIAL_DOMAIN = 'sc.com'
CSV_RANK = 331

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
