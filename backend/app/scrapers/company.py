"""Dispatch a manifest-backed company scraper by its official domain."""
import inspect

from .company_registry import COMPANY_SCRAPERS


def scrape(domain, known_job_ids=None):
    key = domain.strip().lower().removeprefix("www.")
    try:
        scraper = COMPANY_SCRAPERS[key]
    except KeyError as exc:
        raise ValueError(f"Unknown company scraper domain: {domain}") from exc

    if known_job_ids is None:
        return scraper()

    # Company-specific scrapers can opt in directly to incremental behavior.
    try:
        if "known_job_ids" in inspect.signature(scraper).parameters:
            return scraper(known_job_ids=known_job_ids)
    except (TypeError, ValueError):
        pass

    # Most generated company wrappers delegate to auto.scrape. Call that shared
    # adapter with the known set so it can forward it to any incremental-capable
    # provider adapter without rewriting hundreds of identical wrappers.
    globals_ = getattr(scraper, "__globals__", {})
    auto_scraper = globals_.get("_auto_scrape")
    careers_url = globals_.get("CAREERS_URL")
    if callable(auto_scraper) and careers_url:
        return auto_scraper(careers_url, known_job_ids=known_job_ids)

    return scraper()
