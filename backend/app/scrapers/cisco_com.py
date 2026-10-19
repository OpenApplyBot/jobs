"""Company-specific scraper for Cisco.
Official careers URL candidate: https://careers.cisco.com/global/en/search-results
Expected company domain: cisco.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cisco'
CAREERS_URL = 'https://jobs.cisco.com/'
OFFICIAL_DOMAIN = 'cisco.com'
CSV_RANK = 26

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
