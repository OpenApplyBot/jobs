"""Company-specific scraper for H&M.
Official careers URL candidate: https://hm.com/careers
Expected company domain: hm.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'H&M'
CAREERS_URL = 'https://hm.com/careers'
OFFICIAL_DOMAIN = 'hm.com'
CSV_RANK = 403

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
