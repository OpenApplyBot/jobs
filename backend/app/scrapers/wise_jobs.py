"""Company-specific scraper for Wise.
Official careers URL candidate: https://wise.jobs/
Expected company domain: wise.jobs
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Wise'
CAREERS_URL = 'https://wise.jobs/'
OFFICIAL_DOMAIN = 'wise.jobs'
CSV_RANK = 112

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
