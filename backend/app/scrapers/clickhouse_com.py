"""Company-specific scraper for ClickHouse.
Official careers URL candidate: https://clickhouse.com/careers
Expected company domain: clickhouse.com
Customize this module with a verified public API/parser after live testing.
"""
from .greenhouse import scrape as _direct_scrape

COMPANY_NAME = 'ClickHouse'
CAREERS_URL = 'https://clickhouse.com/careers'
OFFICIAL_DOMAIN = 'clickhouse.com'
CSV_RANK = 70

def scrape(token: str | None = None):
    """Fetch live public listings from the verified Greenhouse board."""
    return _direct_scrape("clickhouse", company=COMPANY_NAME)
