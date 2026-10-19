"""Company-specific scraper for NVIDIA.
Official careers URL candidate: https://www.nvidia.com/en-us/about-nvidia/careers/
Expected company domain: nvidia.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'NVIDIA'
CAREERS_URL = 'https://www.nvidia.com/en-us/about-nvidia/careers/'
OFFICIAL_DOMAIN = 'nvidia.com'
CSV_RANK = 7

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
