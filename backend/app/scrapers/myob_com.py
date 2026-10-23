"""Company-specific scraper for MYOB.
Official job-listing URL: https://careers.myob.com/explore-roles
Expected company domain: myob.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'MYOB'
CAREERS_URL = 'https://careers.myob.com/explore-roles'
OFFICIAL_DOMAIN = 'myob.com'
CSV_RANK = 444

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
