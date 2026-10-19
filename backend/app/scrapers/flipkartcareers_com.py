"""Company-specific scraper for Flipkart.
Official careers URL candidate: https://www.flipkartcareers.com/
Expected company domain: flipkartcareers.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Flipkart'
CAREERS_URL = 'https://www.flipkartcareers.com/'
OFFICIAL_DOMAIN = 'flipkartcareers.com'
CSV_RANK = 179

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
