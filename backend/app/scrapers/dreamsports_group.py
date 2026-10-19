"""Company-specific scraper for Dream11.
Official careers URL candidate: https://dreamsports.group/careers
Expected company domain: dreamsports.group
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Dream11'
CAREERS_URL = 'https://dreamsports.group/careers'
OFFICIAL_DOMAIN = 'dreamsports.group'
CSV_RANK = 199

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
