"""xAI Careers scraper using the public Greenhouse job-board API.

The xAI careers page exposes public job pages under job-boards.greenhouse.io/xai.
"""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "xAI"
CAREERS_URL = "https://x.ai/careers"
BOARD_TOKEN = "xai"
OFFICIAL_DOMAIN = "x.ai"
CSV_RANK = 10


def scrape(token: str | None = None):
    """Fetch xAI's public Greenhouse postings; token can override the board slug."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_greenhouse(board)
