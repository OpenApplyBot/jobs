"""Company-specific scraper for Mistral AI.
Official careers URL candidate: https://mistral.ai/careers
Expected company domain: mistral.ai
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Mistral AI'
CAREERS_URL = 'https://mistral.ai/careers'
OFFICIAL_DOMAIN = 'mistral.ai'
CSV_RANK = 55

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
