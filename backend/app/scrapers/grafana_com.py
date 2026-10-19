"""Grafana Labs scraper using its verified public Greenhouse job board."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Grafana Labs"
CAREERS_URL = "https://grafana.com/about/careers/"
BOARD_TOKEN = "grafanalabs"
OFFICIAL_DOMAIN = "grafana.com"
CSV_RANK = 97


def scrape(token: str | None = None):
    """Fetch Grafana Labs's public Greenhouse postings."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_greenhouse(board, company=COMPANY_NAME)
