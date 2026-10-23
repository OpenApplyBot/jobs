"""Company-specific scraper for Zalando.
Official job-listing URL: https://jobs.zalando.com/en/jobs
Expected company domain: zalando.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Zalando'
CAREERS_URL = 'https://jobs.zalando.com/en/jobs'
OFFICIAL_DOMAIN = 'zalando.com'
CSV_RANK = 404

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
