"""Company-specific scraper for Perplexity.
Official careers URL candidate: https://perplexity.ai/careers
Expected company domain: perplexity.ai
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Perplexity'
CAREERS_URL = 'https://perplexity.ai/careers'
OFFICIAL_DOMAIN = 'perplexity.ai'
CSV_RANK = 57

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
