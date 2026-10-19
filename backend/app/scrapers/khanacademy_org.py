"""Company-specific scraper for Khan Academy.
Official careers URL candidate: https://khanacademy.org/careers
Expected company domain: khanacademy.org
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Khan Academy'
CAREERS_URL = 'https://khanacademy.org/careers'
OFFICIAL_DOMAIN = 'khanacademy.org'
CSV_RANK = 309

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
