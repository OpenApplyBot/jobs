"""Company-specific scraper for Wells Fargo.
Official careers URL candidate: https://wellsfargo.com/careers
Expected company domain: wellsfargo.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Wells Fargo'
CAREERS_URL = 'https://wellsfargo.com/careers'
OFFICIAL_DOMAIN = 'wellsfargo.com'
CSV_RANK = 325

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
