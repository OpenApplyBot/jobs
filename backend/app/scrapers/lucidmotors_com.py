"""Company-specific scraper for Lucid Motors.
Official careers URL candidate: https://lucidmotors.com/careers
Expected company domain: lucidmotors.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Lucid Motors'
CAREERS_URL = 'https://lucidmotors.com/careers'
OFFICIAL_DOMAIN = 'lucidmotors.com'
CSV_RANK = 365

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
