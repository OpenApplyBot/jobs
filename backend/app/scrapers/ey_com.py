"""Company-specific scraper for EY.
Official careers URL candidate: https://ey.com/careers
Expected company domain: ey.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'EY'
CAREERS_URL = 'https://ey.com/careers'
OFFICIAL_DOMAIN = 'ey.com'
CSV_RANK = 165

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
