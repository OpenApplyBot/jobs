"""Company-specific scraper for Traveloka.
Official job-listing URL: https://careers.traveloka.com/jobs
Expected company domain: traveloka.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Traveloka'
CAREERS_URL = 'https://careers.traveloka.com/jobs'
OFFICIAL_DOMAIN = 'traveloka.com'
CSV_RANK = 436

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
