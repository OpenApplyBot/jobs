"""Company-specific scraper for Games24x7.
Official careers URL candidate: https://games24x7.com/careers
Expected company domain: games24x7.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Games24x7'
CAREERS_URL = 'https://games24x7.com/careers'
OFFICIAL_DOMAIN = 'games24x7.com'
CSV_RANK = 200

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
