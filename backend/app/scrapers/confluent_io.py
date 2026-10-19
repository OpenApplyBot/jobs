"""Company-specific scraper for Confluent.
Official careers URL candidate: https://confluent.io/careers
Expected company domain: confluent.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Confluent'
CAREERS_URL = 'https://confluent.io/careers'
OFFICIAL_DOMAIN = 'confluent.io'
CSV_RANK = 66

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
