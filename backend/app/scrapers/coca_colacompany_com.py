"""Company-specific scraper for Coca-Cola.
Official job-listing URL: https://coke.wd1.myworkdayjobs.com/coca-cola-careers
Expected company domain: coca-colacompany.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Coca-Cola'
CAREERS_URL = 'https://coke.wd1.myworkdayjobs.com/coca-cola-careers'
OFFICIAL_DOMAIN = 'coca-colacompany.com'
CSV_RANK = 411

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
