"""Company-specific scraper for SoundCloud.
Official careers URL candidate: https://soundcloud.com/careers
Expected company domain: soundcloud.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'SoundCloud'
CAREERS_URL = 'https://soundcloud.com/careers'
OFFICIAL_DOMAIN = 'soundcloud.com'
CSV_RANK = 271

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
