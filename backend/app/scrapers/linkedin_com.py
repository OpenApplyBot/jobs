"""Company-specific scraper for LinkedIn.
Official careers URL candidate: https://linkedin.com/careers
Expected company domain: linkedin.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'LinkedIn'
CAREERS_URL = 'https://linkedin.com/careers'
OFFICIAL_DOMAIN = 'linkedin.com'
CSV_RANK = 319

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
