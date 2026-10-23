"""Company-specific scraper for Vodafone.
Official job-listing URL: https://jobs.vodafone.com/careers?start=0&pid=563018698278962&sort_by=timestamp
Expected company domain: vodafone.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Vodafone'
CAREERS_URL = 'https://jobs.vodafone.com/careers?start=0&pid=563018698278962&sort_by=timestamp'
OFFICIAL_DOMAIN = 'vodafone.com'
CSV_RANK = 446

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
