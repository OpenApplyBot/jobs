"""Company-specific scraper for LatentView Analytics.
Official careers URL candidate: https://latentview.com/careers
Expected company domain: latentview.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'LatentView Analytics'
CAREERS_URL = 'https://latentview.com/careers'
OFFICIAL_DOMAIN = 'latentview.com'
CSV_RANK = 243

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
