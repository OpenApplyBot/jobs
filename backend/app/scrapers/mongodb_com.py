"""Company-specific scraper for MongoDB.
Official careers URL candidate: https://mongodb.com/careers
Expected company domain: mongodb.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'MongoDB'
CAREERS_URL = 'https://mongodb.com/careers'
OFFICIAL_DOMAIN = 'mongodb.com'
CSV_RANK = 64

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
