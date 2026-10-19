"""Company-specific scraper for Nubank.
Official careers URL candidate: https://nubank.com.br/careers
Expected company domain: nubank.com.br
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Nubank'
CAREERS_URL = 'https://nubank.com.br/careers'
OFFICIAL_DOMAIN = 'nubank.com.br'
CSV_RANK = 126

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
