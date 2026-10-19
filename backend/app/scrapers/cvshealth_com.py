"""Company-specific scraper for CVS Health.
Official careers URL candidate: https://cvshealth.com/careers
Expected company domain: cvshealth.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'CVS Health'
CAREERS_URL = 'https://cvshealth.com/careers'
OFFICIAL_DOMAIN = 'cvshealth.com'
CSV_RANK = 397

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
