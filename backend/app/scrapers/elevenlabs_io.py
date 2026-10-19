"""Company-specific scraper for ElevenLabs.
Official careers URL candidate: https://elevenlabs.io/careers
Expected company domain: elevenlabs.io
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'ElevenLabs'
CAREERS_URL = 'https://elevenlabs.io/careers'
OFFICIAL_DOMAIN = 'elevenlabs.io'
CSV_RANK = 60

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
