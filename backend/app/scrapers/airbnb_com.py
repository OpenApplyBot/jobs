"""Airbnb scraper using its verified public Greenhouse job board."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Airbnb"
CAREERS_URL = "https://careers.airbnb.com/"
BOARD_TOKEN = "airbnb"
OFFICIAL_DOMAIN = "airbnb.com"
CSV_RANK = 257


def scrape(token: str | None = None):
    """Fetch Airbnb's public Greenhouse postings."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_greenhouse(board, company=COMPANY_NAME)
