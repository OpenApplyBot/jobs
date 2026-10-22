"""Company-specific scraper for Naver.
Official job-listing URL: https://recruit.navercorp.com/rcrt/list.do?sw=
Expected company domain: navercorp.com
The shared adapter discovers supported ATS feeds and paginates public listing pages.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Naver'
CAREERS_URL = 'https://recruit.navercorp.com/rcrt/list.do?sw='
OFFICIAL_DOMAIN = 'navercorp.com'
CSV_RANK = 440

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
