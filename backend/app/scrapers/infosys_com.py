"""Company-specific scraper for Infosys.
Official careers URL candidate: https://www.infosys.com/careers
Expected company domain: infosys.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Infosys'
CAREERS_URL = 'https://www.infosys.com/careers'
OFFICIAL_DOMAIN = 'infosys.com'
CSV_RANK = 138

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
