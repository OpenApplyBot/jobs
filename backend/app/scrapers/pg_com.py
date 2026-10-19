"""Company-specific scraper for Procter & Gamble.
Official careers URL candidate: https://pg.com/careers
Expected company domain: pg.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Procter & Gamble'
CAREERS_URL = 'https://pg.com/careers'
OFFICIAL_DOMAIN = 'pg.com'
CSV_RANK = 408

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
