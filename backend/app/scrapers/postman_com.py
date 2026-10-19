"""Company-specific scraper for Postman.
Official careers URL candidate: https://www.postman.com/company/careers/open-positions/
Expected company domain: postman.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Postman'
CAREERS_URL = 'https://postman.com/careers'
OFFICIAL_DOMAIN = 'postman.com'
CSV_RANK = 83

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
