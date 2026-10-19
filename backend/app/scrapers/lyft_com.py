"""Lyft scraper using its verified public Greenhouse job board."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Lyft"
CAREERS_URL = "https://www.lyft.com/careers"
BOARD_TOKEN = "lyft"
OFFICIAL_DOMAIN = "lyft.com"
CSV_RANK = 258


def scrape(token: str | None = None):
    """Fetch Lyft's public Greenhouse postings."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_greenhouse(board, company=COMPANY_NAME)
