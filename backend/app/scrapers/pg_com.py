"""Company-specific scraper for Procter & Gamble.
Official job-listing URL: https://www.pgcareers.com/in/en/engineering-new#search-results
Expected company domain: pg.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Procter & Gamble'
CAREERS_URL = 'https://www.pgcareers.com/in/en/engineering-new#search-results'
OFFICIAL_DOMAIN = 'pg.com'
CSV_RANK = 408

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
