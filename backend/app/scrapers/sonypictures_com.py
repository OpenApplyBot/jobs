"""Company-specific scraper for Sony Pictures.
Official careers URL candidate: https://sonypictures.com/careers
Expected company domain: sonypictures.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Sony Pictures'
CAREERS_URL = 'https://sonypictures.com/careers'
OFFICIAL_DOMAIN = 'sonypictures.com'
CSV_RANK = 479

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
