"""Company-specific scraper for Twitch.
Official careers URL candidate: https://twitch.tv/careers
Expected company domain: twitch.tv
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Twitch'
CAREERS_URL = 'https://twitch.tv/careers'
OFFICIAL_DOMAIN = 'twitch.tv'
CSV_RANK = 272

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
