"""Company-specific scraper for Dropbox.
Official careers URL candidate: https://www.dropbox.jobs/
Expected company domain: dropbox.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Dropbox'
CAREERS_URL = 'https://www.dropbox.jobs/'
OFFICIAL_DOMAIN = 'dropbox.com'
CSV_RANK = 284

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
