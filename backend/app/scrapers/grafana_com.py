"""Company-specific scraper for Grafana Labs.
Official careers URL candidate: https://grafana.com/careers
Expected company domain: grafana.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Grafana Labs'
CAREERS_URL = 'https://grafana.com/careers'
OFFICIAL_DOMAIN = 'grafana.com'
CSV_RANK = 97

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
