"""Company-specific scraper for GitLab.
Official careers URL candidate: https://about.gitlab.com/jobs/
Expected company domain: gitlab.com
Customize this module with a verified public API/parser after live testing.
"""
from .greenhouse import scrape as _direct_scrape

COMPANY_NAME = 'GitLab'
CAREERS_URL = 'https://about.gitlab.com/jobs/'
OFFICIAL_DOMAIN = 'gitlab.com'
CSV_RANK = 79

def scrape(token: str | None = None):
    """Fetch live public listings from the verified Greenhouse board."""
    return _direct_scrape("gitlab", company=COMPANY_NAME)
