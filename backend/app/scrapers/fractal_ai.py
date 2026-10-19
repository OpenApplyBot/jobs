"""Company-specific scraper for Fractal.
Official careers URL candidate: https://fractal.ai/careers
Expected company domain: fractal.ai
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Fractal'
CAREERS_URL = 'https://fractal.ai/careers'
OFFICIAL_DOMAIN = 'fractal.ai'
CSV_RANK = 239

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
