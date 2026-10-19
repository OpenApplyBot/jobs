"""Company-specific scraper for PhonePe.
Official careers URL candidate: https://www.phonepe.com/careers/
Expected company domain: phonepe.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'PhonePe'
CAREERS_URL = 'https://www.phonepe.com/careers/'
OFFICIAL_DOMAIN = 'phonepe.com'
CSV_RANK = 190

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
