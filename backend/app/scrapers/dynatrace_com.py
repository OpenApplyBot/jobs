"""Company-specific scraper for Dynatrace.
Official careers URL candidate: https://dynatrace.com/careers
Expected company domain: dynatrace.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Dynatrace'
CAREERS_URL = 'https://dynatrace.com/careers'
OFFICIAL_DOMAIN = 'dynatrace.com'
CSV_RANK = 100

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
