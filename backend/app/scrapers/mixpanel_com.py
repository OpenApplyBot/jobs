"""Company-specific scraper for Mixpanel.
Official careers URL candidate: https://mixpanel.com/careers
Expected company domain: mixpanel.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Mixpanel'
CAREERS_URL = 'https://mixpanel.com/careers'
OFFICIAL_DOMAIN = 'mixpanel.com'
CSV_RANK = 107

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
