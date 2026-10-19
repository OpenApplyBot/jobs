"""Company-specific scraper for Zepto.
Official careers URL candidate: https://zeptonow.com/careers
Expected company domain: zeptonow.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zepto'
CAREERS_URL = 'https://zeptonow.com/careers'
OFFICIAL_DOMAIN = 'zeptonow.com'
CSV_RANK = 183

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
