"""Company-specific scraper for Yandex.
Official careers URL candidate: https://yandex.com/careers
Expected company domain: yandex.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Yandex'
CAREERS_URL = 'https://yandex.com/careers'
OFFICIAL_DOMAIN = 'yandex.com'
CSV_RANK = 452

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
