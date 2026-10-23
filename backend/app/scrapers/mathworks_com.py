"""Company-specific scraper for MathWorks.
Official job-listing URL: https://in.mathworks.com/company/jobs/opportunities/search/
Expected company domain: mathworks.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'MathWorks'
CAREERS_URL = 'https://in.mathworks.com/company/jobs/opportunities/search/'
OFFICIAL_DOMAIN = 'mathworks.com'
CSV_RANK = 427

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
