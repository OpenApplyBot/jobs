"""TikTok Careers scraper based on its current official global search page.

The public search portal is lifeattiktok.com/search. Use the shared same-site
JSON-LD and job-link parser rather than assuming an undocumented API endpoint.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = "TikTok"
CAREERS_URL = "https://lifeattiktok.com/search/?language=en"
OFFICIAL_DOMAIN = "tiktok.com"
CSV_RANK = 12


def scrape(token: str | None = None):
    """Fetch public TikTok listings from the official careers search page."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    return _auto_scrape(url)
