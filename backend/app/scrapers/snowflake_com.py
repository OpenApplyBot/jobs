"""Snowflake scraper using its official public Greenhouse job board API."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Snowflake"
CAREERS_URL = "https://boards.greenhouse.io/snowflake"
OFFICIAL_DOMAIN = "greenhouse.io"
CSV_RANK = 51

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "snowflake"
    return _scrape_greenhouse(board, company=COMPANY_NAME)
