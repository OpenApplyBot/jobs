"""Company-specific scraper for Mercado Libre.
Official careers URL candidate: https://mercadolibre.com/careers
Expected company domain: mercadolibre.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Mercado Libre'
CAREERS_URL = 'https://mercadolibre.com/careers'
OFFICIAL_DOMAIN = 'mercadolibre.com'
CSV_RANK = 438

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
