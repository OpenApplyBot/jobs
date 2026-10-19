"""OpenAI Careers scraper using the public Ashby job-board API.

The official OpenAI careers page links its open roles to jobs.ashbyhq.com/openai.
"""
from .ashby import scrape as _scrape_ashby

COMPANY_NAME = "OpenAI"
CAREERS_URL = "https://openai.com/careers/search/"
BOARD_TOKEN = "openai"
OFFICIAL_DOMAIN = "openai.com"
CSV_RANK = 8


def scrape(token: str | None = None):
    """Fetch OpenAI's public Ashby postings; token can override the board slug."""
    board = token.strip() if token and token.strip() else BOARD_TOKEN
    return _scrape_ashby(board)
