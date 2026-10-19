"""Company-specific scraper for Tiger Analytics.
Official careers URL candidate: https://tigeranalytics.com/careers
Expected company domain: tigeranalytics.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tiger Analytics'
CAREERS_URL = 'https://tigeranalytics.com/careers'
OFFICIAL_DOMAIN = 'tigeranalytics.com'
CSV_RANK = 240

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
