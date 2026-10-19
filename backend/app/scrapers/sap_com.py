"""Company-specific scraper for SAP.
Official careers URL candidate: https://jobs.sap.com/
Expected company domain: sap.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'SAP'
CAREERS_URL = 'https://jobs.sap.com/'
OFFICIAL_DOMAIN = 'sap.com'
CSV_RANK = 25

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
