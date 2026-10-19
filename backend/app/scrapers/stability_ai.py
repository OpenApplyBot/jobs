"""Stability AI scraper using its official public Greenhouse job board API."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Stability AI"
CAREERS_URL = "https://boards.greenhouse.io/stabilityai"
OFFICIAL_DOMAIN = "greenhouse.io"
CSV_RANK = 59

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "stabilityai"
    return _scrape_greenhouse(board, company=COMPANY_NAME)
