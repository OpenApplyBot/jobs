"""Company-specific scraper for INDmoney.
Official careers URL candidate: https://indmoney.com/careers
Expected company domain: indmoney.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'INDmoney'
CAREERS_URL = 'https://indmoney.com/careers'
OFFICIAL_DOMAIN = 'indmoney.com'
CSV_RANK = 230

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
