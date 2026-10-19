"""Company-specific scraper for Proofpoint.
Official careers URL candidate: https://proofpoint.com/careers
Expected company domain: proofpoint.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Proofpoint'
CAREERS_URL = 'https://proofpoint.com/careers'
OFFICIAL_DOMAIN = 'proofpoint.com'
CSV_RANK = 459

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
