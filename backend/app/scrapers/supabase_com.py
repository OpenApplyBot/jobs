"""Company-specific scraper for Supabase.
Official careers URL candidate: https://supabase.com/careers
Expected company domain: supabase.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Supabase'
CAREERS_URL = 'https://supabase.com/careers'
OFFICIAL_DOMAIN = 'supabase.com'
CSV_RANK = 72

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
