"""Company-specific scraper for NTT DATA.
Official careers URL candidate: https://www.nttdata.com/en-us/careers
Expected company domain: nttdata.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'NTT DATA'
CAREERS_URL = 'https://www.nttdata.com/en-us/careers'
OFFICIAL_DOMAIN = 'nttdata.com'
CSV_RANK = 161

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
