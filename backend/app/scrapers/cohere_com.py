"""Company-specific scraper for Cohere.
Official careers URL candidate: https://cohere.com/careers
Expected company domain: cohere.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cohere'
CAREERS_URL = 'https://cohere.com/careers'
OFFICIAL_DOMAIN = 'cohere.com'
CSV_RANK = 54

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
