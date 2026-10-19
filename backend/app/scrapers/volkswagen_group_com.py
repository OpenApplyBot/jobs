"""Company-specific scraper for Volkswagen.
Official careers URL candidate: https://jobs.volkswagen-group.com/VWGIS/?locale=en_US
Expected company domain: volkswagen-group.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Volkswagen'
CAREERS_URL = 'https://jobs.volkswagen-group.com/VWGIS/?locale=en_US'
OFFICIAL_DOMAIN = 'volkswagen-group.com'
CSV_RANK = 360

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
