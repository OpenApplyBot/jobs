"""Company-specific scraper for GE Aerospace.
Official careers URL candidate: https://geaerospace.com/careers
Expected company domain: geaerospace.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'GE Aerospace'
CAREERS_URL = 'https://geaerospace.com/careers'
OFFICIAL_DOMAIN = 'geaerospace.com'
CSV_RANK = 355

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
