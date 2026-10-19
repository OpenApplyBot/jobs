"""Company-specific scraper for DigitalOcean.
Official careers URL candidate: https://digitalocean.com/careers
Expected company domain: digitalocean.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'DigitalOcean'
CAREERS_URL = 'https://digitalocean.com/careers'
OFFICIAL_DOMAIN = 'digitalocean.com'
CSV_RANK = 297

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
