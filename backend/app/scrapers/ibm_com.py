"""Company-specific scraper for IBM.
Official careers URL candidate: https://ibm.com/careers
Expected company domain: ibm.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'IBM'
CAREERS_URL = 'https://ibm.com/careers'
OFFICIAL_DOMAIN = 'ibm.com'
CSV_RANK = 21

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
