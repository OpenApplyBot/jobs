"""Company-specific scraper for Juniper Networks.
Official careers URL candidate: https://juniper.net/careers
Expected company domain: juniper.net
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Juniper Networks'
CAREERS_URL = 'https://juniper.net/careers'
OFFICIAL_DOMAIN = 'juniper.net'
CSV_RANK = 45

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
