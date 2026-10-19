"""Company-specific scraper for Observe.AI.
Official careers URL candidate: https://observe.ai/careers
Expected company domain: observe.ai
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Observe.AI'
CAREERS_URL = 'https://observe.ai/careers'
OFFICIAL_DOMAIN = 'observe.ai'
CSV_RANK = 236

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
