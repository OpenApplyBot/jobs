"""Company-specific scraper for Notion.
Official careers URL candidate: https://notion.com/careers
Expected company domain: notion.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Notion'
CAREERS_URL = 'https://notion.com/careers'
OFFICIAL_DOMAIN = 'notion.com'
CSV_RANK = 86

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
