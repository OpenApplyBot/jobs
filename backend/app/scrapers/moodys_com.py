"""Company-specific scraper for Moody's.
Official careers URL candidate: https://moodys.com/careers
Expected company domain: moodys.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = "Moody's"
CAREERS_URL = 'https://moodys.com/careers'
OFFICIAL_DOMAIN = 'moodys.com'
CSV_RANK = 339

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
