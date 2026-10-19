"""Company-specific scraper for Discord.
Official careers URL candidate: https://discord.com/careers
Expected company domain: discord.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Discord'
CAREERS_URL = 'https://discord.com/careers'
OFFICIAL_DOMAIN = 'discord.com'
CSV_RANK = 489

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
