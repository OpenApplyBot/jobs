"""Company-specific scraper for Red Hat.
Official careers URL candidate: https://redhat.com/careers
Expected company domain: redhat.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Red Hat'
CAREERS_URL = 'https://redhat.com/careers'
OFFICIAL_DOMAIN = 'redhat.com'
CSV_RANK = 48

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
