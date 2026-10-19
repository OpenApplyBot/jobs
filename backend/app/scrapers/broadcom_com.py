"""Company-specific scraper for Broadcom.
Official careers URL candidate: https://careers.broadcom.com/careers-home/jobs
Expected company domain: broadcom.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Broadcom'
CAREERS_URL = 'https://broadcom.com/careers'
OFFICIAL_DOMAIN = 'broadcom.com'
CSV_RANK = 35

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
