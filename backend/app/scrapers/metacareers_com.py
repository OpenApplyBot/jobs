"""Company-specific scraper for Meta.
Official careers URL candidate: https://www.metacareers.com/
Expected company domain: metacareers.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Meta'
CAREERS_URL = 'https://www.metacareers.com/'
OFFICIAL_DOMAIN = 'metacareers.com'
CSV_RANK = 5

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
