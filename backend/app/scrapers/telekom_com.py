"""Company-specific scraper for Deutsche Telekom.
Official careers URL candidate: https://careers.telekom.com/en
Expected company domain: telekom.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Deutsche Telekom'
CAREERS_URL = 'https://careers.telekom.com/en'
OFFICIAL_DOMAIN = 'telekom.com'
CSV_RANK = 449

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
