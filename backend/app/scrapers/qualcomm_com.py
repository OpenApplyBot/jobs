"""Company-specific scraper for Qualcomm.
Official careers URL candidate: https://qualcomm.com/careers
Expected company domain: qualcomm.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Qualcomm'
CAREERS_URL = 'https://qualcomm.com/careers'
OFFICIAL_DOMAIN = 'qualcomm.com'
CSV_RANK = 29

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
