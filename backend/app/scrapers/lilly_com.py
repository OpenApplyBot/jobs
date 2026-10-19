"""Company-specific scraper for Eli Lilly.
Official careers URL candidate: https://lilly.com/careers
Expected company domain: lilly.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Eli Lilly'
CAREERS_URL = 'https://lilly.com/careers'
OFFICIAL_DOMAIN = 'lilly.com'
CSV_RANK = 392

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
