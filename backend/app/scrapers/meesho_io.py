"""Company-specific scraper for Meesho.
Official careers URL candidate: https://www.meesho.io/jobs
Expected company domain: meesho.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Meesho'
CAREERS_URL = 'https://www.meesho.io/jobs'
OFFICIAL_DOMAIN = 'meesho.io'
CSV_RANK = 178

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
