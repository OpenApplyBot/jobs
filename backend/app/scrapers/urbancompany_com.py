"""Company-specific scraper for Urban Company.
Official careers URL candidate: https://urbancompany.com/careers
Expected company domain: urbancompany.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Urban Company'
CAREERS_URL = 'https://urbancompany.com/careers'
OFFICIAL_DOMAIN = 'urbancompany.com'
CSV_RANK = 212

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
