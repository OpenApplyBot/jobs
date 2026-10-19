"""Alibaba Group careers scraper using the official public position-list page.

The group portal's homepage is a business-unit directory, not the job list.
Use the official off-campus position-list route with the shared parser; if the
page requires client-side session state, the scraper returns no records rather
than inventing jobs or bypassing access controls.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = "Alibaba"
CAREERS_URL = "https://talent.alibaba.com/off-campus/position-list?lang=zh"
OFFICIAL_DOMAIN = "alibaba.com"
CSV_RANK = 14


def scrape(token: str | None = None):
    """Fetch public listings from Alibaba's official position-list page."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    return _auto_scrape(url)
