"""Company-specific scraper for Miro.
Official careers URL candidate: https://miro.com/careers
Expected company domain: miro.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Miro'
CAREERS_URL = 'https://miro.com/careers'
OFFICIAL_DOMAIN = 'miro.com'
CSV_RANK = 89

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
