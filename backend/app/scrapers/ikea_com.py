"""Company-specific scraper for IKEA.
Official careers URL candidate: https://jobs.ikea.com/
Expected company domain: ikea.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'IKEA'
CAREERS_URL = 'https://jobs.ikea.com/'
OFFICIAL_DOMAIN = 'ikea.com'
CSV_RANK = 402

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
