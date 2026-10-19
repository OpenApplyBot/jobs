"""Company-specific scraper for 1Password.
Official careers URL candidate: https://1password.com/careers
Expected company domain: 1password.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = '1Password'
CAREERS_URL = 'https://1password.com/careers'
OFFICIAL_DOMAIN = '1password.com'
CSV_RANK = 94

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
