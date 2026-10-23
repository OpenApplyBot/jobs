"""Company-specific scraper for AstraZeneca.
Official job-listing URL: https://careers.astrazeneca.com/search-jobs
Expected company domain: astrazeneca.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'AstraZeneca'
CAREERS_URL = 'https://careers.astrazeneca.com/search-jobs'
OFFICIAL_DOMAIN = 'astrazeneca.com'
CSV_RANK = 388

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
