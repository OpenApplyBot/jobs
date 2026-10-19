"""Figma scraper using its verified public Greenhouse job board.

Figma's official careers page links open roles to job-boards.greenhouse.io/figma.
"""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Figma"
CAREERS_URL = "https://www.figma.com/careers/"
BOARD_TOKEN = "figma"
OFFICIAL_DOMAIN = "figma.com"
CSV_RANK = 84


def scrape(token: str | None = None):
    """Fetch Figma's public Greenhouse listings."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_greenhouse(board, company=COMPANY_NAME)
