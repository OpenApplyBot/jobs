"""Company-specific scraper for CVS Health.
Official job-listing URL: https://jobs.cvshealth.com/us/en/search-results
Expected company domain: cvshealth.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'CVS Health'
CAREERS_URL = 'https://jobs.cvshealth.com/us/en/search-results'
OFFICIAL_DOMAIN = 'cvshealth.com'
CSV_RANK = 397

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
