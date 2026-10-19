"""Company-specific scraper for TikTok.
Official careers URL candidate: https://tiktok.com/careers
Expected company domain: tiktok.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'TikTok'
CAREERS_URL = 'https://tiktok.com/careers'
OFFICIAL_DOMAIN = 'tiktok.com'
CSV_RANK = 12

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
