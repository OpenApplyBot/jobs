"""Hugging Face scraper using its official public Greenhouse job board API."""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Hugging Face"
CAREERS_URL = "https://boards.greenhouse.io/huggingface"
OFFICIAL_DOMAIN = "greenhouse.io"
CSV_RANK = 56

def scrape(token: str | None = None):
    board = token.strip() if token and token.strip() else "huggingface"
    return _scrape_greenhouse(board, company=COMPANY_NAME)
