"""Company-specific scraper for Nazara Technologies.
Official careers URL candidate: https://nazara.com/careers
Expected company domain: nazara.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Nazara Technologies'
CAREERS_URL = 'https://nazara.com/careers'
OFFICIAL_DOMAIN = 'nazara.com'
CSV_RANK = 201

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
