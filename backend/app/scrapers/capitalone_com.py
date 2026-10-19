"""Company-specific scraper for Capital One.
Official careers URL candidate: https://capitalone.com/careers
Expected company domain: capitalone.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Capital One'
CAREERS_URL = 'https://capitalone.com/careers'
OFFICIAL_DOMAIN = 'capitalone.com'
CSV_RANK = 323

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
