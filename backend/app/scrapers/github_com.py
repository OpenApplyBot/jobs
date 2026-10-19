"""Company-specific scraper for GitHub.
Official careers URL candidate: https://github.careers/
Expected company domain: github.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'GitHub'
CAREERS_URL = 'https://www.github.careers/careers-home/jobs'
OFFICIAL_DOMAIN = 'github.com'
CSV_RANK = 78

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
