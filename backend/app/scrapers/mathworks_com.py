"""Company-specific scraper for MathWorks.
Official careers URL candidate: https://mathworks.com/careers
Expected company domain: mathworks.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'MathWorks'
CAREERS_URL = 'https://mathworks.com/careers'
OFFICIAL_DOMAIN = 'mathworks.com'
CSV_RANK = 427

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
