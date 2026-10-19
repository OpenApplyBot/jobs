"""Company-specific scraper for Autodesk.
Official careers URL candidate: https://autodesk.com/careers
Expected company domain: autodesk.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Autodesk'
CAREERS_URL = 'https://autodesk.com/careers'
OFFICIAL_DOMAIN = 'autodesk.com'
CSV_RANK = 422

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
