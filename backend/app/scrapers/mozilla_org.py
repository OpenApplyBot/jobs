"""Mozilla scraper using its verified public Greenhouse job board."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Mozilla"
CAREERS_URL = "https://www.mozilla.org/careers/"
BOARD_TOKEN = "mozilla"
OFFICIAL_DOMAIN = "mozilla.org"
CSV_RANK = 491


def scrape(token: str | None = None):
    """Fetch Mozilla's public Greenhouse postings."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_greenhouse(board, company=COMPANY_NAME)
