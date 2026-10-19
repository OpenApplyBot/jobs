"""Company-specific scraper for HERE Technologies.
Official careers URL candidate: https://here.com/careers
Expected company domain: here.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'HERE Technologies'
CAREERS_URL = 'https://here.com/careers'
OFFICIAL_DOMAIN = 'here.com'
CSV_RANK = 429

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
