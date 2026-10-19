"""Company-specific scraper for Neo4j.
Official careers URL candidate: https://neo4j.com/careers
Expected company domain: neo4j.com
Customize this module with a verified public API/parser after live testing.
"""
from .greenhouse import scrape as _direct_scrape

COMPANY_NAME = 'Neo4j'
CAREERS_URL = 'https://neo4j.com/careers'
OFFICIAL_DOMAIN = 'neo4j.com'
CSV_RANK = 69

def scrape(token: str | None = None):
    """Fetch live public listings from the verified Greenhouse board."""
    return _direct_scrape("neo4j", company=COMPANY_NAME)
