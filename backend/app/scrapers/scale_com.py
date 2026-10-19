"""Scale AI scraper using its official public Greenhouse job board API."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Scale AI"
CAREERS_URL = "https://boards.greenhouse.io/scaleai"
OFFICIAL_DOMAIN = "greenhouse.io"
CSV_RANK = 53

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "scaleai"
    return _scrape_greenhouse(board, company=COMPANY_NAME)
