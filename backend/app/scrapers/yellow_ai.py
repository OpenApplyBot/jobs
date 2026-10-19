"""Company-specific scraper for Yellow.ai.
Official careers URL candidate: https://yellow.ai/careers
Expected company domain: yellow.ai
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Yellow.ai'
CAREERS_URL = 'https://yellow.ai/careers'
OFFICIAL_DOMAIN = 'yellow.ai'
CSV_RANK = 235

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
