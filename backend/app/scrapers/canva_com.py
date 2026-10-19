"""Company-specific scraper for Canva.
Official careers URL candidate: https://canva.com/careers
Expected company domain: canva.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Canva'
CAREERS_URL = 'https://canva.com/careers'
OFFICIAL_DOMAIN = 'canva.com'
CSV_RANK = 85

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
