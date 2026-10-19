"""Canva scraper using its verified public SmartRecruiters board.

The official careers site links to careers.smartrecruiters.com/Canva. The
SmartRecruiters adapter accepts the company slug, not a careers-page URL.
"""
from .smartrecruiters import scrape as _direct_scrape

COMPANY_NAME = "Canva"
CAREERS_URL = "https://careers.smartrecruiters.com/Canva"
BOARD_TOKEN = "Canva"
OFFICIAL_DOMAIN = "canva.com"
CSV_RANK = 85


def scrape(token: str | None = None):
    """Fetch Canva's public SmartRecruiters postings."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _direct_scrape(board)
