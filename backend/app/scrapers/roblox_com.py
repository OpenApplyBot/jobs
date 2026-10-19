"""Company-specific scraper for Roblox.
Official careers URL candidate: https://roblox.com/careers
Expected company domain: roblox.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Roblox'
CAREERS_URL = 'https://roblox.com/careers'
OFFICIAL_DOMAIN = 'roblox.com'
CSV_RANK = 273

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
