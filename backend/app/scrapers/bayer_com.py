"""Company-specific scraper for Bayer.
Official job-listing URL: https://bayer.eightfold.ai/careers?query=&location=&hl=en
Expected company domain: bayer.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Bayer'
CAREERS_URL = 'https://bayer.eightfold.ai/careers?query=&location=&hl=en'
OFFICIAL_DOMAIN = 'bayer.com'
CSV_RANK = 394

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
