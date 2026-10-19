"""Company-specific scraper for LaunchDarkly.
Official careers URL candidate: https://launchdarkly.com/careers
Expected company domain: launchdarkly.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'LaunchDarkly'
CAREERS_URL = 'https://launchdarkly.com/careers'
OFFICIAL_DOMAIN = 'launchdarkly.com'
CSV_RANK = 105

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
