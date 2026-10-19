"""Company-specific scraper for Synopsys.
Official careers URL candidate: https://synopsys.com/careers
Expected company domain: synopsys.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Synopsys'
CAREERS_URL = 'https://synopsys.com/careers'
OFFICIAL_DOMAIN = 'synopsys.com'
CSV_RANK = 41

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
