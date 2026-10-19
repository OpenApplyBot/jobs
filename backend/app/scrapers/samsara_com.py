"""Samsara scraper using its verified public Greenhouse job board."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Samsara"
CAREERS_URL = "https://www.samsara.com/company/careers"
BOARD_TOKEN = "samsara"
OFFICIAL_DOMAIN = "samsara.com"
CSV_RANK = 420


def scrape(token: str | None = None):
    """Fetch Samsara's public Greenhouse postings."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_greenhouse(board, company=COMPANY_NAME)
