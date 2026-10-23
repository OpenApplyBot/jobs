"""Company-specific scraper for BT Group.
Official job-listing URL: https://jobs.bt.com/search/?q=&locationsearch=&
Expected company domain: bt.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'BT Group'
CAREERS_URL = 'https://jobs.bt.com/search/?q=&locationsearch=&'
OFFICIAL_DOMAIN = 'bt.com'
CSV_RANK = 448

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
