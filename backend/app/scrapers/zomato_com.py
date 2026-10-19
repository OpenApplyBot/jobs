"""Company-specific scraper for Zomato.
Official careers URL candidate: https://www.zomato.com/careers
Expected company domain: zomato.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zomato'
CAREERS_URL = 'https://www.zomato.com/careers'
OFFICIAL_DOMAIN = 'zomato.com'
CSV_RANK = 182

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
