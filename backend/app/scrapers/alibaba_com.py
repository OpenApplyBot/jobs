"""Alibaba Group careers scraper using the official recruitment portal.

The official group portal is talent.alibaba.com, not alibaba.com/careers.
It is a portal for multiple Alibaba business groups, so results depend on the
public job links exposed by the current portal and its linked career systems.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = "Alibaba"
CAREERS_URL = "https://talent.alibaba.com/en/home?page_id=27"
OFFICIAL_DOMAIN = "alibaba.com"
CSV_RANK = 14


def scrape(token: str | None = None):
    """Fetch listings from Alibaba's official recruitment portal."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    return _auto_scrape(url)
