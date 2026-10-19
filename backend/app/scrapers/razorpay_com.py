"""Company-specific scraper for Razorpay.
Official careers URL candidate: https://razorpay.com/jobs/
Expected company domain: razorpay.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Razorpay'
CAREERS_URL = 'https://razorpay.com/jobs/'
OFFICIAL_DOMAIN = 'razorpay.com'
CSV_RANK = 186

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
