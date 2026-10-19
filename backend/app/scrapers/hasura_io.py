"""Company-specific scraper for Hasura.
Official careers URL candidate: https://hasura.io/careers
Expected company domain: hasura.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Hasura'
CAREERS_URL = 'https://hasura.io/careers'
OFFICIAL_DOMAIN = 'hasura.io'
CSV_RANK = 173

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
