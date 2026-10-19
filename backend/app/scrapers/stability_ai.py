"""Company-specific scraper for Stability AI.
Official careers URL candidate: https://stability.ai/careers
Expected company domain: stability.ai
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Stability AI'
CAREERS_URL = 'https://stability.ai/careers'
OFFICIAL_DOMAIN = 'stability.ai'
CSV_RANK = 59

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
