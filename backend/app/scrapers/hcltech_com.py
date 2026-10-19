"""Company-specific scraper for HCLTech.
Official careers URL candidate: https://careers.hcltech.com/
Expected company domain: hcltech.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'HCLTech'
CAREERS_URL = 'https://careers.hcltech.com/'
OFFICIAL_DOMAIN = 'hcltech.com'
CSV_RANK = 140

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
