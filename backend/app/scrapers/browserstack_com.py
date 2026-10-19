"""Company-specific scraper for BrowserStack.
Official careers URL candidate: https://www.browserstack.com/careers
Expected company domain: browserstack.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'BrowserStack'
CAREERS_URL = 'https://www.browserstack.com/careers'
OFFICIAL_DOMAIN = 'browserstack.com'
CSV_RANK = 169

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
