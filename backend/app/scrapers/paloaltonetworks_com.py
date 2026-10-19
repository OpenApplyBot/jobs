"""Company-specific scraper for Palo Alto Networks.
Official careers URL candidate: https://paloaltonetworks.com/careers
Expected company domain: paloaltonetworks.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Palo Alto Networks'
CAREERS_URL = 'https://paloaltonetworks.com/careers'
OFFICIAL_DOMAIN = 'paloaltonetworks.com'
CSV_RANK = 292

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
