"""Company-specific scraper for Goldman Sachs.
Official careers URL candidate: https://goldmansachs.com/careers
Expected company domain: goldmansachs.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Goldman Sachs'
CAREERS_URL = 'https://goldmansachs.com/careers'
OFFICIAL_DOMAIN = 'goldmansachs.com'
CSV_RANK = 129

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
