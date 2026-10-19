"""NVIDIA Careers scraper using the official Workday job-search API.

NVIDIA's public careers frontend links candidates to its Workday-hosted
external career site. This adapter uses that same public site, including
Workday pagination and per-job detail enrichment.
"""
from .workday import scrape as _scrape_workday

COMPANY_NAME = "NVIDIA"
CAREERS_URL = "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite"
OFFICIAL_DOMAIN = "nvidia.com"
CSV_RANK = 7


def scrape(token: str | None = None):
    """Fetch current NVIDIA listings; an explicit Workday URL may override the default."""
    url = token.strip() if token and token.strip() else CAREERS_URL
    return _scrape_workday(url)
