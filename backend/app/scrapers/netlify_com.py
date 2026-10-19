"""Company-specific scraper for Netlify.
Official careers URL candidate: https://netlify.com/careers
Expected company domain: netlify.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Netlify'
CAREERS_URL = 'https://netlify.com/careers'
OFFICIAL_DOMAIN = 'netlify.com'
CSV_RANK = 74

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
