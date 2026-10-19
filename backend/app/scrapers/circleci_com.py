"""Company-specific scraper for CircleCI.
Official careers URL candidate: https://circleci.com/careers
Expected company domain: circleci.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'CircleCI'
CAREERS_URL = 'https://circleci.com/careers'
OFFICIAL_DOMAIN = 'circleci.com'
CSV_RANK = 104

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
