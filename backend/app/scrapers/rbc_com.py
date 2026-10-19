"""Company-specific scraper for RBC.
Official careers URL candidate: https://rbc.com/careers
Expected company domain: rbc.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'RBC'
CAREERS_URL = 'https://rbc.com/careers'
OFFICIAL_DOMAIN = 'rbc.com'
CSV_RANK = 347

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
