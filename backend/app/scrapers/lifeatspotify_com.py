"""Company-specific scraper for Spotify.
Official careers URL candidate: https://www.lifeatspotify.com/jobs
Expected company domain: lifeatspotify.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Spotify'
CAREERS_URL = 'https://www.lifeatspotify.com/jobs'
OFFICIAL_DOMAIN = 'lifeatspotify.com'
CSV_RANK = 270

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
