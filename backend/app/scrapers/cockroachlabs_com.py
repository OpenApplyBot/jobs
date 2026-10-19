"""Company-specific scraper for Cockroach Labs.
Official careers URL candidate: https://cockroachlabs.com/careers
Expected company domain: cockroachlabs.com
Customize this module with a verified public API/parser after live testing.
"""
from .greenhouse import scrape as _direct_scrape

COMPANY_NAME = 'Cockroach Labs'
CAREERS_URL = 'https://cockroachlabs.com/careers'
OFFICIAL_DOMAIN = 'cockroachlabs.com'
CSV_RANK = 68

def scrape(token: str | None = None):
    """Fetch live public listings from the verified Greenhouse board."""
    return _direct_scrape("cockroachlabs", company=COMPANY_NAME)
