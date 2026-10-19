"""Company-specific scraper for Huawei.
Official careers URL candidate: https://huawei.com/careers
Expected company domain: huawei.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Huawei'
CAREERS_URL = 'https://huawei.com/careers'
OFFICIAL_DOMAIN = 'huawei.com'
CSV_RANK = 16

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
