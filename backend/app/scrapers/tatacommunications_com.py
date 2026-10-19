"""Company-specific scraper for Tata Communications.
Official careers URL candidate: https://tatacommunications.com/careers
Expected company domain: tatacommunications.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Tata Communications'
CAREERS_URL = 'https://tatacommunications.com/careers'
OFFICIAL_DOMAIN = 'tatacommunications.com'
CSV_RANK = 221

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
