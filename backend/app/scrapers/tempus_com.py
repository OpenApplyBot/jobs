"""Company-specific scraper for Tempus AI.
Official job-listing URL: https://tempus.wd5.myworkdayjobs.com/Tempus_Careers
Expected company domain: tempus.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tempus AI'
CAREERS_URL = 'https://tempus.wd5.myworkdayjobs.com/Tempus_Careers'
OFFICIAL_DOMAIN = 'tempus.com'
CSV_RANK = 401

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
