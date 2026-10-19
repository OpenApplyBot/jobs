"""Company-specific scraper for SoFi.
Official careers URL candidate: https://sofi.com/careers
Expected company domain: sofi.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'SoFi'
CAREERS_URL = 'https://sofi.com/careers'
OFFICIAL_DOMAIN = 'sofi.com'
CSV_RANK = 127

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
