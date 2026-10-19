"""Asana scraper using its verified public Greenhouse job board."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Asana"
CAREERS_URL = "https://asana.com/jobs"
BOARD_TOKEN = "asana"
OFFICIAL_DOMAIN = "asana.com"
CSV_RANK = 91


def scrape(token: str | None = None):
    """Fetch Asana's public Greenhouse postings."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_greenhouse(board, company=COMPANY_NAME)
