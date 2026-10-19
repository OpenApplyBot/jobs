"""Company-specific scraper for xAI.
Official careers URL candidate: https://x.ai/careers
Expected company domain: x.ai
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'xAI'
CAREERS_URL = 'https://x.ai/careers'
OFFICIAL_DOMAIN = 'x.ai'
CSV_RANK = 10

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
