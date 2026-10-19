"""Company-specific scraper for MoEngage.
Official careers URL candidate: https://moengage.com/careers
Expected company domain: moengage.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'MoEngage'
CAREERS_URL = 'https://moengage.com/careers'
OFFICIAL_DOMAIN = 'moengage.com'
CSV_RANK = 250

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
