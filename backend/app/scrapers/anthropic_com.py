"""Anthropic Careers scraper using the public Greenhouse job-board API.

Anthropic's official careers listings link directly to job-boards.greenhouse.io/anthropic.
"""
from .greenhouse import scrape as _scrape_greenhouse

COMPANY_NAME = "Anthropic"
CAREERS_URL = "https://www.anthropic.com/careers/jobs"
BOARD_TOKEN = "anthropic"
OFFICIAL_DOMAIN = "anthropic.com"
CSV_RANK = 9


def scrape(token: str | None = None):
    """Fetch Anthropic's public Greenhouse postings; token can override the board slug."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_greenhouse(board)
