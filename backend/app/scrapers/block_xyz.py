"""Company-specific scraper for Block.
Official careers URL candidate: https://block.xyz/careers
Expected company domain: block.xyz
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Block'
CAREERS_URL = 'https://block.xyz/careers'
OFFICIAL_DOMAIN = 'block.xyz'
CSV_RANK = 111

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
