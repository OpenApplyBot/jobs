"""Company-specific scraper for Snowflake.
Official careers URL candidate: https://snowflake.com/careers
Expected company domain: snowflake.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Snowflake'
CAREERS_URL = 'https://snowflake.com/careers'
OFFICIAL_DOMAIN = 'snowflake.com'
CSV_RANK = 51

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
