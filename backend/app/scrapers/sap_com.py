"""SAP Careers scraper using SAP's current public careers site.
The company is migrating roles from the legacy jobs.sap.com site to careers.sap.com.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'SAP'
CAREERS_URL = 'https://careers.sap.com/en/'
OFFICIAL_DOMAIN = 'sap.com'
CSV_RANK = 25

def scrape(token: str | None = None):
    """Fetch current public listings; an explicit URL token overrides the default."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
