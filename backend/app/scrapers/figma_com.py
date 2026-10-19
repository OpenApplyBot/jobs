"""Company-specific scraper for Figma.
Official careers URL candidate: https://figma.com/careers
Expected company domain: figma.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Figma'
CAREERS_URL = 'https://figma.com/careers'
OFFICIAL_DOMAIN = 'figma.com'
CSV_RANK = 84

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
