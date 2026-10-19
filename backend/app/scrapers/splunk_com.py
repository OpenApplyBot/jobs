"""Company-specific scraper for Splunk.
Official careers URL candidate: https://splunk.com/careers
Expected company domain: splunk.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Splunk'
CAREERS_URL = 'https://splunk.com/careers'
OFFICIAL_DOMAIN = 'splunk.com'
CSV_RANK = 99

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
