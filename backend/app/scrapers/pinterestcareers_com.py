"""Company-specific scraper for Pinterest.
Official careers URL candidate: https://pinterestcareers.com/careers
Expected company domain: pinterestcareers.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Pinterest'
CAREERS_URL = 'https://pinterestcareers.com/careers'
OFFICIAL_DOMAIN = 'pinterestcareers.com'
CSV_RANK = 487

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
