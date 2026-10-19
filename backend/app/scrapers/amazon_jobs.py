"""Company-specific scraper for Amazon.
Official careers URL candidate: https://www.amazon.jobs/
Expected company domain: amazon.jobs
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Amazon'
CAREERS_URL = 'https://www.amazon.jobs/'
OFFICIAL_DOMAIN = 'amazon.jobs'
CSV_RANK = 3

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
