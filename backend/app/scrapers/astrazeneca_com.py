"""Company-specific scraper for AstraZeneca.
Official careers URL candidate: https://astrazeneca.com/careers
Expected company domain: astrazeneca.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'AstraZeneca'
CAREERS_URL = 'https://astrazeneca.com/careers'
OFFICIAL_DOMAIN = 'astrazeneca.com'
CSV_RANK = 388

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
