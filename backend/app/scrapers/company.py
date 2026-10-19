"""Dispatch a manifest-backed company scraper by its official domain."""
from .company_registry import COMPANY_SCRAPERS


def scrape(domain):
    key = domain.strip().lower().removeprefix("www.")
    try:
        scraper = COMPANY_SCRAPERS[key]
    except KeyError as exc:
        raise ValueError(f"Unknown company scraper domain: {domain}") from exc
    return scraper()
