"""Company-specific scraper for Ansys.
Official careers URL candidate: https://ansys.com/careers
Expected company domain: ansys.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Ansys'
CAREERS_URL = 'https://ansys.com/careers'
OFFICIAL_DOMAIN = 'ansys.com'
CSV_RANK = 426

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
