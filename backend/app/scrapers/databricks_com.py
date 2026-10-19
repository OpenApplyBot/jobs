"""Databricks scraper using its official public Greenhouse job board API."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Databricks"
CAREERS_URL = "https://boards.greenhouse.io/databricks"
OFFICIAL_DOMAIN = "greenhouse.io"
CSV_RANK = 50

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "databricks"
    return _scrape_greenhouse(board, company=COMPANY_NAME)
