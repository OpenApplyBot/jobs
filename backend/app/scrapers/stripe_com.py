"""Company-specific scraper for Stripe.
Official careers URL candidate: https://stripe.com/jobs
Expected company domain: stripe.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Stripe'
CAREERS_URL = 'https://stripe.com/jobs'
OFFICIAL_DOMAIN = 'stripe.com'
CSV_RANK = 110

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
