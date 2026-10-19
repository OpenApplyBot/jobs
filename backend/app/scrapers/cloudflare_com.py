"""Company-specific scraper for Cloudflare.
Official careers URL candidate: https://www.cloudflare.com/careers/
Expected company domain: cloudflare.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Cloudflare'
CAREERS_URL = 'https://www.cloudflare.com/careers/'
OFFICIAL_DOMAIN = 'cloudflare.com'
CSV_RANK = 75

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
