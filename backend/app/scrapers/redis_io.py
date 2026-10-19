"""Company-specific scraper for Redis.
Official careers URL candidate: https://redis.io/careers
Expected company domain: redis.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Redis'
CAREERS_URL = 'https://redis.io/careers'
OFFICIAL_DOMAIN = 'redis.io'
CSV_RANK = 67

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
