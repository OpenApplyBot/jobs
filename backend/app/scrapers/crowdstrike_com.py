"""Company-specific scraper for CrowdStrike.
Official careers URL candidate: https://crowdstrike.com/careers
Expected company domain: crowdstrike.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'CrowdStrike'
CAREERS_URL = 'https://crowdstrike.com/careers'
OFFICIAL_DOMAIN = 'crowdstrike.com'
CSV_RANK = 291

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
