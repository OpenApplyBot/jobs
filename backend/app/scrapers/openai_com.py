"""Company-specific scraper for OpenAI.
Official careers URL candidate: https://openai.com/careers/
Expected company domain: openai.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'OpenAI'
CAREERS_URL = 'https://openai.com/careers/'
OFFICIAL_DOMAIN = 'openai.com'
CSV_RANK = 8

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
