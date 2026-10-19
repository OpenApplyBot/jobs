"""Company-specific scraper for Naver.
Official careers URL candidate: https://navercorp.com/careers
Expected company domain: navercorp.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Naver'
CAREERS_URL = 'https://navercorp.com/careers'
OFFICIAL_DOMAIN = 'navercorp.com'
CSV_RANK = 440

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
