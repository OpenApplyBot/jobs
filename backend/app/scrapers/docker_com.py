"""Company-specific scraper for Docker.
Official careers URL candidate: https://docker.com/careers
Expected company domain: docker.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Docker'
CAREERS_URL = 'https://docker.com/careers'
OFFICIAL_DOMAIN = 'docker.com'
CSV_RANK = 82

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
