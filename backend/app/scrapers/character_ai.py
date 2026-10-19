"""Company-specific scraper for Character.AI.
Official careers URL candidate: https://character.ai/careers
Expected company domain: character.ai
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Character.AI'
CAREERS_URL = 'https://character.ai/careers'
OFFICIAL_DOMAIN = 'character.ai'
CSV_RANK = 61

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
