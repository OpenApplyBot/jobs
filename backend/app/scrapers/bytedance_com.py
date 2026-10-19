"""Company-specific scraper for ByteDance.
Official careers URL candidate: https://bytedance.com/careers
Expected company domain: bytedance.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ByteDance'
CAREERS_URL = 'https://bytedance.com/careers'
OFFICIAL_DOMAIN = 'bytedance.com'
CSV_RANK = 11

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
