"""Company-specific scraper for Sonar.
Official careers URL candidate: https://sonarsource.com/careers
Expected company domain: sonarsource.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Sonar'
CAREERS_URL = 'https://sonarsource.com/careers'
OFFICIAL_DOMAIN = 'sonarsource.com'
CSV_RANK = 103

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
