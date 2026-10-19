"""Company-specific scraper for Confluent.
Official careers URL candidate: https://confluent.io/careers
Expected company domain: confluent.io
Customize this module with a verified public API/parser after live testing.
"""
from .ashby import scrape as _direct_scrape

COMPANY_NAME = 'Confluent'
CAREERS_URL = 'https://confluent.io/careers'
OFFICIAL_DOMAIN = 'confluent.io'
CSV_RANK = 66

def scrape(token: str | None = None, known_job_ids=None):
    """Fetch live public listings from the verified Ashby board."""
    return _direct_scrape("confluent", company=COMPANY_NAME, known_job_ids=known_job_ids)
