"""Company-specific scraper for Fastly.
Official careers URL candidate: https://fastly.com/careers
Expected company domain: fastly.com
Customize this module with a verified public API/parser after live testing.
"""
from .greenhouse import scrape as _direct_scrape

COMPANY_NAME = 'Fastly'
CAREERS_URL = 'https://fastly.com/careers'
OFFICIAL_DOMAIN = 'fastly.com'
CSV_RANK = 76

def scrape(token: str | None = None):
    """Fetch live public listings from the verified Greenhouse board."""
    return _direct_scrape("fastly", company=COMPANY_NAME)
