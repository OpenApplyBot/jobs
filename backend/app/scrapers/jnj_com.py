"""Company-specific scraper for Johnson & Johnson.
Official job-listing URL: https://www.careers.jnj.com/en/jobs/?search
Expected company domain: jnj.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Johnson & Johnson'
CAREERS_URL = 'https://www.careers.jnj.com/en/jobs/?search'
OFFICIAL_DOMAIN = 'jnj.com'
CSV_RANK = 391

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
