"""Company-specific scraper for FactSet.
Official careers URL candidate: https://factset.com/careers
Expected company domain: factset.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'FactSet'
CAREERS_URL = 'https://factset.com/careers'
OFFICIAL_DOMAIN = 'factset.com'
CSV_RANK = 135

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
