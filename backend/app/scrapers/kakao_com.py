"""Company-specific scraper for Kakao.
Official careers URL candidate: https://kakao.com/careers
Expected company domain: kakao.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Kakao'
CAREERS_URL = 'https://kakao.com/careers'
OFFICIAL_DOMAIN = 'kakao.com'
CSV_RANK = 439

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
