"""Company-specific scraper for Hugging Face.
Official careers URL candidate: https://huggingface.co/careers
Expected company domain: huggingface.co
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Hugging Face'
CAREERS_URL = 'https://huggingface.co/careers'
OFFICIAL_DOMAIN = 'huggingface.co'
CSV_RANK = 56

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
