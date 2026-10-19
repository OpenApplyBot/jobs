"""Company-specific scraper for Ather Energy.
Official careers URL candidate: https://atherenergy.com/careers
Expected company domain: atherenergy.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Ather Energy'
CAREERS_URL = 'https://atherenergy.com/careers'
OFFICIAL_DOMAIN = 'atherenergy.com'
CSV_RANK = 209

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
