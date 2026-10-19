"""Company-specific scraper for NBCUniversal.
Official careers URL candidate: https://nbcuniversal.com/careers
Expected company domain: nbcuniversal.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'NBCUniversal'
CAREERS_URL = 'https://nbcuniversal.com/careers'
OFFICIAL_DOMAIN = 'nbcuniversal.com'
CSV_RANK = 477

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
