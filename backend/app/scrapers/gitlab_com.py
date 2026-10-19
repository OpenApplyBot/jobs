"""Company-specific scraper for GitLab.
Official careers URL candidate: https://about.gitlab.com/jobs/
Expected company domain: gitlab.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'GitLab'
CAREERS_URL = 'https://about.gitlab.com/jobs/'
OFFICIAL_DOMAIN = 'gitlab.com'
CSV_RANK = 79

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
