"""Company-specific scraper for Neo4j.
Official careers URL candidate: https://neo4j.com/careers
Expected company domain: neo4j.com
Customize this module with a verified public API/parser after live testing.
"""
from .auto import scrape as _auto_scrape

COMPANY_NAME = 'Neo4j'
CAREERS_URL = 'https://neo4j.com/careers'
OFFICIAL_DOMAIN = 'neo4j.com'
CSV_RANK = 69

def scrape(token: str | None = None):
    """Fetch current public listings. An explicit URL token overrides the CSV URL."""
    return _auto_scrape(token.strip() if token and token.strip() else CAREERS_URL)
