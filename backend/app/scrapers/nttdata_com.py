"""Company-specific scraper for NTT DATA.
Official careers URL candidate: https://nttdata.com/careers
Expected company domain: nttdata.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'NTT DATA'
CAREERS_URL = 'https://nttdata.com/careers'
OFFICIAL_DOMAIN = 'nttdata.com'
CSV_RANK = 161

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
