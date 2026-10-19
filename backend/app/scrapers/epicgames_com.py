"""Company-specific scraper for Epic Games.
Official careers URL candidate: https://epicgames.com/careers
Expected company domain: epicgames.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Epic Games'
CAREERS_URL = 'https://epicgames.com/careers'
OFFICIAL_DOMAIN = 'epicgames.com'
CSV_RANK = 274

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
