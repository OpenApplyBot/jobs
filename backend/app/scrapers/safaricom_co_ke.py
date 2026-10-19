"""Company-specific scraper for Safaricom.
Official careers URL candidate: https://safaricom.co.ke/careers
Expected company domain: safaricom.co.ke
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Safaricom'
CAREERS_URL = 'https://safaricom.co.ke/careers'
OFFICIAL_DOMAIN = 'safaricom.co.ke'
CSV_RANK = 451

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
