"""Company-specific scraper for DocuSign.
Official careers URL candidate: https://docusign.com/careers
Expected company domain: docusign.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'DocuSign'
CAREERS_URL = 'https://docusign.com/careers'
OFFICIAL_DOMAIN = 'docusign.com'
CSV_RANK = 283

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
