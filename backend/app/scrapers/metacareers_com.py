"""Meta Careers scraper using the official public jobs listing route.

Meta's root page is a marketing page; the public listings live under /jobs/.
This adapter only parses publicly returned job data and does not bypass login
walls or access controls.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = "Meta"
CAREERS_URL = "https://www.metacareers.com/jobs/"
OFFICIAL_DOMAIN = "metacareers.com"
CSV_RANK = 5


def scrape(token: str | None = None):
    """Fetch Meta's public jobs listing page."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    return _auto_scrape(url)
