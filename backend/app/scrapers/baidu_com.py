"""Company-specific scraper for Baidu.
Official careers URL candidate: https://baidu.com/careers
Expected company domain: baidu.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Baidu'
CAREERS_URL = 'https://baidu.com/careers'
OFFICIAL_DOMAIN = 'baidu.com'
CSV_RANK = 15

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
