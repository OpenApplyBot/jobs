"""Company-specific scraper for Redis.
Official careers URL candidate: https://redis.io/careers
Expected company domain: redis.io
Customize this module with a verified public API/parser after live testing.
"""
from .ashby import scrape as _direct_scrape

COMPANY_NAME = 'Redis'
CAREERS_URL = 'https://redis.io/careers'
OFFICIAL_DOMAIN = 'redis.io'
CSV_RANK = 67

def scrape(token: str | None = None, known_job_ids=None):
    """Fetch live public listings from the verified Ashby board."""
    return _direct_scrape("redis", company=COMPANY_NAME, known_job_ids=known_job_ids)
