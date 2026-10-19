"""Company-specific scraper for Signal.
Official careers URL candidate: https://signal.org/careers
Expected company domain: signal.org
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Signal'
CAREERS_URL = 'https://signal.org/careers'
OFFICIAL_DOMAIN = 'signal.org'
CSV_RANK = 490

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
