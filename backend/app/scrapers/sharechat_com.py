"""Company-specific scraper for ShareChat.
Official careers URL candidate: https://sharechat.com/careers
Expected company domain: sharechat.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ShareChat'
CAREERS_URL = 'https://sharechat.com/careers'
OFFICIAL_DOMAIN = 'sharechat.com'
CSV_RANK = 177

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
