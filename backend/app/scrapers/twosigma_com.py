"""Company-specific scraper for Two Sigma.
Official careers URL candidate: https://twosigma.com/careers
Expected company domain: twosigma.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Two Sigma'
CAREERS_URL = 'https://twosigma.com/careers'
OFFICIAL_DOMAIN = 'twosigma.com'
CSV_RANK = 133

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
