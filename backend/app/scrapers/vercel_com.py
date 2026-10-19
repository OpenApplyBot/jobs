"""Company-specific scraper for Vercel.
Official careers URL candidate: https://vercel.com/careers
Expected company domain: vercel.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Vercel'
CAREERS_URL = 'https://vercel.com/careers'
OFFICIAL_DOMAIN = 'vercel.com'
CSV_RANK = 73

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
