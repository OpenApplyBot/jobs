"""Company-specific scraper for Twilio.
Official careers URL candidate: https://twilio.com/careers
Expected company domain: twilio.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Twilio'
CAREERS_URL = 'https://twilio.com/careers'
OFFICIAL_DOMAIN = 'twilio.com'
CSV_RANK = 289

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
