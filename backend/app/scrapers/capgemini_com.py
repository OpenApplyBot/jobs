"""Company-specific scraper for Capgemini.
Official careers URL candidate: https://capgemini.com/careers
Expected company domain: capgemini.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Capgemini'
CAREERS_URL = 'https://capgemini.com/careers'
OFFICIAL_DOMAIN = 'capgemini.com'
CSV_RANK = 158

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
