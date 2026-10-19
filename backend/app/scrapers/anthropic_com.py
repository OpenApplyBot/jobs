"""Company-specific scraper for Anthropic.
Official careers URL candidate: https://www.anthropic.com/careers
Expected company domain: anthropic.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Anthropic'
CAREERS_URL = 'https://www.anthropic.com/careers'
OFFICIAL_DOMAIN = 'anthropic.com'
CSV_RANK = 9

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
