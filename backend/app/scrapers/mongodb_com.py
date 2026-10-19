"""MongoDB scraper using its official public Greenhouse job board API."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "MongoDB"
CAREERS_URL = "https://boards.greenhouse.io/mongodb"
OFFICIAL_DOMAIN = "greenhouse.io"
CSV_RANK = 64

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "mongodb"
    return _scrape_greenhouse(board, company=COMPANY_NAME)
