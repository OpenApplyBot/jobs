"""Registry for isolated public job scrapers."""
import inspect

from .scrapers import greenhouse,lever,ashby,smartrecruiters,workable,recruitee,workday,remoteok,remotive,arbeitnow,themuse,jobicy,himalayas,jsonld,auto,company
SCRAPERS={"greenhouse":greenhouse.scrape,"lever":lever.scrape,"ashby":ashby.scrape,"smartrecruiters":smartrecruiters.scrape,"workable":workable.scrape,"recruitee":recruitee.scrape,"workday":workday.scrape,"remoteok":remoteok.scrape,"remotive":remotive.scrape,"arbeitnow":arbeitnow.scrape,"themuse":themuse.scrape,"jobicy":jobicy.scrape,"himalayas":himalayas.scrape,"jsonld":jsonld.scrape,"auto":auto.scrape,"company":company.scrape}
CONNECTORS=tuple(sorted(SCRAPERS))


class JobFetchResult(list):
    """List-compatible normalized results with optional scraper capability metadata."""

    def __init__(self, jobs=(), *, incremental_ready=None, verified_unchanged_ids=None):
        super().__init__(jobs)
        self.incremental_ready = incremental_ready
        self.verified_unchanged_ids = set(verified_unchanged_ids or ())


def fetch_jobs(connector, token, known_job_ids=None, known_job_hashes=None):
    """Fetch normalized jobs, forwarding known IDs to adapters that support deltas."""
    name = connector.strip().lower()
    if name not in SCRAPERS:
        raise ValueError(f"Unsupported connector: {name}. Supported: {', '.join(CONNECTORS)}")
    from .scrapers.common import normalize

    scraper = SCRAPERS[name]
    kwargs = {}
    if known_job_ids is not None:
        try:
            parameters = inspect.signature(scraper).parameters.values()
            if any(p.name == "known_job_ids" or p.kind == inspect.Parameter.VAR_KEYWORD for p in parameters):
                kwargs["known_job_ids"] = known_job_ids
        except (TypeError, ValueError):
            pass
    scraped_rows = scraper(token.strip(), **kwargs)
    incremental_ready = getattr(scraped_rows, "incremental_ready", None)
    rows = scraped_rows or []
    verified_unchanged_ids = set()
    result = JobFetchResult(incremental_ready=incremental_ready)
    seen = set()
    known_hashes = known_job_hashes or {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        item = normalize(
            row.get("source_job_id"), row.get("title"), row.get("url"), row.get("location"),
            row.get("department"), row.get("employment_type"), row.get("description"),
            row.get("posted_at"), row.get("company_name"),
            raw_payload=row.get("raw_payload", row), apply_url=row.get("apply_url"),
        )
        if not item or not item["title"] or not item["url"]:
            continue
        sid = item["source_job_id"]
        if sid in seen:
            continue
        seen.add(sid)
        if sid in known_hashes and known_hashes[sid] and item["content_hash"] == known_hashes[sid]:
            # The live listing's stable material fingerprint matches the active
            # database record. Report it for lightweight bulk verification instead
            # of passing the full record through the ORM update/snapshot loop.
            verified_unchanged_ids.add(sid)
            continue
        result.append(item)
    result.verified_unchanged_ids = verified_unchanged_ids
    return result
