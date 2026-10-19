"""Company-specific scraper for Booking.com.
Official careers URL candidate: https://booking.com/careers
Expected company domain: booking.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Booking.com'
CAREERS_URL = 'https://booking.com/careers'
OFFICIAL_DOMAIN = 'booking.com'
CSV_RANK = 266

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
