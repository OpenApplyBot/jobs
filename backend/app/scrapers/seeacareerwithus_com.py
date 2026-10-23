"""Company-specific scraper for Coca-Cola Consolidated.

Official job-listing URL: https://www.seeacareerwithus.com/search-jobs#search-results
Expected company domain: seeacareerwithus.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = "Coca-Cola Consolidated"
CAREERS_URL = "https://www.seeacareerwithus.com/search-jobs#search-results"
OFFICIAL_DOMAIN = "seeacareerwithus.com"
CSV_RANK = 501


def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the default URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
