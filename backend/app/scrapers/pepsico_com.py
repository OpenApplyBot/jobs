"""Company-specific scraper for PepsiCo.
Official job-listing URL: https://www.pepsicojobs.com/main/jobs
Expected company domain: pepsico.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'PepsiCo'
CAREERS_URL = 'https://www.pepsicojobs.com/main/jobs'
OFFICIAL_DOMAIN = 'pepsico.com'
CSV_RANK = 412

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
