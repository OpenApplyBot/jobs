"""Company-specific scraper for Kaspersky.
Official careers URL candidate: https://careers.kaspersky.com/vacancies
Expected company domain: kaspersky.com
Uses the official careers portal; ATS discovery is performed by the shared adapter.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Kaspersky'
CAREERS_URL = 'https://careers.kaspersky.com/vacancies'
OFFICIAL_DOMAIN = 'kaspersky.com'
CSV_RANK = 453

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
