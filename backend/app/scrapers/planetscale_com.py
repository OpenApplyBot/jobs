"""Company-specific scraper for PlanetScale.
Official careers URL candidate: https://planetscale.com/careers
Expected company domain: planetscale.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'PlanetScale'
CAREERS_URL = 'https://planetscale.com/careers'
OFFICIAL_DOMAIN = 'planetscale.com'
CSV_RANK = 71

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
