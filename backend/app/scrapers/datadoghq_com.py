"""Company-specific scraper for Datadog.
Official careers URL candidate: https://datadoghq.com/careers
Expected company domain: datadoghq.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Datadog'
CAREERS_URL = 'https://datadoghq.com/careers'
OFFICIAL_DOMAIN = 'datadoghq.com'
CSV_RANK = 96

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
