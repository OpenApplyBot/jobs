"""Company-specific scraper for Tech Mahindra.
Official careers URL candidate: https://careers.techmahindra.com/
Expected company domain: techmahindra.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tech Mahindra'
CAREERS_URL = 'https://careers.techmahindra.com/'
OFFICIAL_DOMAIN = 'techmahindra.com'
CSV_RANK = 141

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
